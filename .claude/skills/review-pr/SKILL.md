---
name: review-pr
description: Review a pull request for correctness, scope, and tests, with severity-tagged findings. Use on every pull request before a human reviews.
---
# Review a pull request

## Steps
1. Read the description. Write down what the change claims to do.
2. Read the whole diff. Then read the tests. Run the tests; paste the summary.
3. For each finding, one line: severity · `path:line` · what is wrong · what would fix it.
   - **must fix** — wrong behavior, missing or weakened test, secret in the diff
   - **should fix** — scope beyond the description, unclear naming, missing doc update
   - **nit** — style
4. End with one of: `ready for human review` or `needs changes (N must-fix)`.

## Rules
- No approval. Humans approve.
- A review without a test run is a read, not a review.
