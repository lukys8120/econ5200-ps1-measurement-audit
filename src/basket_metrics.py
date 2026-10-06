"""Audit and robust-average tools for the basket-value metric."""

import numpy as np
import pandas as pd
from scipy import stats


def audit_report(df: pd.DataFrame, iqr_k: float = 1.5) -> pd.DataFrame:
    """Summarise data quality, one row per column of df.

    Parameters
    ----------
    df : pd.DataFrame
        The table to audit.
    iqr_k : float
        Outlier fence multiplier: a value is an outlier if it lies more than
        iqr_k * IQR below Q1 or above Q3.

    Returns
    -------
    pd.DataFrame
        Indexed by column name, with missing_pct, dtype, skew and n_outliers.
        Skew and outliers are NaN and 0 for non-numeric and boolean columns.
    """
    rows = {}
    for col in df.columns:
        s = df[col]
        is_numeric = pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s)

        if is_numeric:
            q1, q3 = s.quantile([0.25, 0.75])
            iqr = q3 - q1
            n_outliers = int(((s < q1 - iqr_k*iqr) | (s > q3 + iqr_k*iqr)).sum())
            skew = float(s.skew())
        else:
            n_outliers = 0
            skew = np.nan

        rows[col] = {'missing_pct': s.isna().mean(), 'dtype': str(s.dtype), 'skew': skew, 'n_outliers': n_outliers}

    return pd.DataFrame.from_dict(rows, orient='index')


def robust_mean(x, method: str = "median", trim: float = 0.1, threshold: float | None = None) -> float:
    """A robust centre for x, ignoring missing values.

    Parameters
    ----------
    x : array-like
        The values to average.
    method : str
        "median", "trimmed" (drops the top and bottom `trim` share before
        averaging) or "exclusion" (the mean of the values at or below
        `threshold`).
    trim : float
        Share cut from each tail when method="trimmed".
    threshold : float, optional
        Cut-off above which values are excluded; required when
        method="exclusion".

    Returns
    -------
    float
        The robust centre.

    Raises
    ------
    ValueError
        If x has no non-missing values, method is unknown, or method is
        "exclusion" without a threshold.
    """
    values = np.asarray(x, dtype=float)
    values = values[~np.isnan(values)]

    if values.size == 0:
        raise ValueError("x has no non-missing values")

    if method == "median":
        return float(np.median(values))
    if method == "trimmed":
        return float(stats.trim_mean(values, trim))
    if method == "exclusion":
        if threshold is None:
            raise ValueError('method="exclusion" needs a threshold')
        return float(values[values <= threshold].mean())

    raise ValueError(f"unknown method: {method!r}")


if __name__ == "__main__":
    rng = np.random.default_rng(0)

    basket_value = rng.lognormal(mean=np.log(50), sigma=0.7, size=5000)
    b2b_value = rng.lognormal(mean=np.log(2000), sigma=0.5, size=20)
    demo = pd.DataFrame({'basket_value': np.concatenate([basket_value, b2b_value])})
    demo.loc[:9, 'basket_value'] = np.nan

    print(audit_report(demo))
    print(f"Mean: {demo['basket_value'].mean():.2f}")
    for method in ["median", "trimmed", "exclusion"]:
        print(f"{method}: {robust_mean(demo['basket_value'], method=method, threshold=500):.2f}")
