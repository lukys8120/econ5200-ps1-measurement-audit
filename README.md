# Econ 5200 PS1: The Measurement Audit

An audit of a retailer's "average basket value" dashboard metric, using simulated transaction data.

## The finding

**Average basket is flat, not up 7.6%**

- **Headline:** the average consumer basket was 64.2 in 2025 against 64.3 in 2024, a change of -0.2%. The dashboard showed +7.6%.
- **Correction:** two things inflated 2025. Large B2B orders made up 4.3 points of the gap, and cancelled orders, which were logged in 2025 but not in 2024, made up 2.8 points (0.4 points comes from the two together). The metric now excludes baskets over 500 and counts completed orders only.
- **Confidence:** high. Any cut-off between 400 and 1,500 gives a result between -0.4% and +0.2%.
- **Still needed before betting on it:** confirmation from the data team that no other logging change happened between years, and a B2B account flag from the CRM so we don't rely on a size threshold.

## What's in the folder

- `Econ_5200_PS1.ipynb`: the notebook. Builds and contaminates the data, reproduces the dashboard number, separates the two causes, and compares robust alternatives.
- `src/basket_metrics.py`: the module, with `audit_report` for a data-quality summary and `robust_mean` for the median, trimmed and exclusion averages.
- `ai-appendix.md`: the Phase 4 AI transcript, with the prompt, the reply, what I rejected and what I changed.
