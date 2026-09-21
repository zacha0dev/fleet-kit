---
name: write-tests-first
description: Write the failing test before the code change. Use at the start of every fix and every feature.
---
# Write tests first

## Steps
1. From the plan or triage, state the behavior in one sentence: "When X, the result is Y."
2. Write one test that asserts exactly that. Name it after the behavior, not the function.
3. Run it. It must fail, and fail for the stated reason. Paste the failure.
4. If it passes already, stop: either the behavior exists or the test is wrong. Report which.

## Rules
- One claim per test.
- No mocking the thing under test.
- The test goes in the same pull request as the fix, committed first.
