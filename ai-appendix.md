# AI Appendix: Phase 4

## The prompt as sent

[Prep] Act as a partner reviewing an analytics deliverable before it
goes to a client board. You are looking for the objection that would
embarrass us in the room.

[Request] I audited a retailer's "average basket value" metric. I found
the naive mean was inflated by a right-skewed B2B tail and by a change
in what was logged between years. I recommend the dashboard show a
trimmed mean with an explicit B2B exclusion rule. Give me the three
strongest objections to that recommendation, ordered by how likely the
client is to raise them, and for each one tell me what evidence would
settle it.

[Iterate] Be specific to this metric. Do not give me generic data
quality advice.

[Mechanism Check] For each objection, say whether it is a question
about the data, about the statistic, or about the business definition
of the metric -- these need different kinds of answer.

[Evaluate] Which single additional analysis would most reduce our
exposure?

## The reply

**1. "You're removing B2B customers, so the number no longer ties to revenue."** *(Business definition)*
This is the most likely objection. The board sees a lower figure that doesn't reconcile to finance and reads the exclusion as hiding revenue. A second risk sits underneath: if B2B is flagged by basket size rather than by account type, the exclusion is just a second trim and is circular.
*Settles it:* evidence that B2B runs as a separate channel with its own owner or KPI, a B2B flag defined by account or invoice type rather than basket value, and a bridge showing B2B's share of baskets versus its share of revenue.

**2. "If logging changed between years, your YoY comparison is broken whatever statistic you use."** *(Data)*
This is the most dangerous objection. Trimming does not fix a definitional break, and our recommendation as written doesn't address it. If a director asks why last year's figure moved, we have no answer.
*Settles it:* the exact nature of the change (for example, returns netting, split tenders, or online and in-store merging), plus a restatement of the prior year under the new definition or an overlap period logged both ways.

**3. "Why trim at X%? It looks like you picked the cut that gives the nicest number."** *(Statistic)*
A CFO or audit-committee member is the one likely to raise this. Trimming also cuts legitimate high-value B2C baskets, such as big-ticket and seasonal purchases.
*Settles it:* a sensitivity table across trim levels (1, 2.5, 5, 10%) and the median, showing that the level and YoY direction stay stable. Also check what share of trimmed baskets are B2C.

**Single analysis that most reduces exposure:**
A like-for-like restated bridge. Restate both years on the new logging definition, then decompose the naive mean into the trimmed B2C mean in steps: logging effect, then B2B mix effect, then tail-trim effect, with trim sensitivity on the last step. This answers all three objections on one page and closes the gap our current recommendation leaves open (objection 2).

## What I rejected

- **Running down objection 2 (logging), which the reply calls the most dangerous.** My recommendation already counts completed orders only, so the logging change is removed, and Phase 2.1 measured its effect at 2.84 pp. The reply assumes our recommendation ignores the logging change, which is true of the prompt's wording but not of my notebook (cell 17).
- **The trim-level sensitivity table (1, 2.5, 5, 10%).** Cell 17 already drops the trimmed mean: it still shows +3.13% growth because trimming cannot remove the cancelled orders, and it cannot be multiplied back into revenue.
- **The restated bridge as the single extra analysis.** Phase 2.1 already decomposes the gap step by step (B2B 4.33 pp, logging 2.84 pp, interaction 0.40 pp, total 7.56 pp), which is the same idea.
- **Evidence that only exists for a real retailer:** a B2B channel owner, account or invoice type, returns netting, split tenders and an overlap period logged both ways. My data is simulated, so none of it exists to check.

## Changes I made

- The prompt says I recommend a trimmed mean → I sent the brief's prompt unchanged, but my actual recommendation (cell 17) is the plain mean after the B2B rule, on completed orders only.
- Objection 3 says the cut looks picked to give the nicest number → I applied that test to my 500 B2B cut-off instead of a trim percentage. Cell 25 sweeps cut-offs from 300 to 5,000, and growth stays between -0.37% and +0.17% across 400 to 1,500, against true growth of +0.02%.
- Objection 1 says a size-based B2B flag is circular → I checked the 500 rule against the `is_b2b` label. It catches 45 of 45 B2B orders and drops 14 of 20,000 consumer orders.
- Objection 1 asks for a B2B flag based on account type → the board slide's "Still needed" bullet asks for a B2B account flag from the CRM.
