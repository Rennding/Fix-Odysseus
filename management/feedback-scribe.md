# External feedback scribe

<!-- Dormant by default. Referenced from CLAUDE.md §2. Read only when the feedback prefix is used or the feature is being activated. -->

This pipeline supports **one external feedback provider** — someone who gives product or business feedback but never builds, plans, or touches code or QA.

## Activating

1. Add a row to `CLAUDE.md` §3 with the provider's name + GitHub handle.
2. Their first name becomes the prefix: `<Name>:`.

Until that row exists, ignore the prefix and treat the message as ordinary input.

## Behavior when `<Name>:` appears

1. Infer category: `feedback:product` (UX, features, output quality) or `feedback:business` (monetization, positioning, growth).
2. Infer priority from urgency and tone; default `P2` when unclear.
3. Open a GitHub issue with this body:

   ```
   **Category:** [Product / Business]
   **From:** <Name>

   ## Feedback
   [One clear paragraph: a structured version of the raw input.]

   ## Suggested Direction
   [Their specific proposal, if any. Omit this section if none.]
   ```

4. Open it under the provider's GitHub account if available, else Aram's. Labels: `feedback` + the subcategory (`feedback:product` / `feedback:business`) + priority. Assign to Aram.
5. Confirm with one line: issue number and title.

The provider may also use `q:`, `quick:`, and `decision:` for product questions, with the same behavior as for Aram (per `CLAUDE.md` §2).
