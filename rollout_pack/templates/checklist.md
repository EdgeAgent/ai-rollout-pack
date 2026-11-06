# Rollout Checklist — __BUSINESS_NAME__

Work top to bottom. Do not skip the governance steps to get to the fun
steps; the governance steps are why the fun steps are safe.

## Day 1 — set up the lane

- [ ] Pick ONE lane to pilot. One lane, one owner, one job.
- [ ] Write the lane's one-pager (`one-pagers/`). If you cannot describe
      the job on one page, the lane is too big — split it.
- [ ] Fill in `memory/MEMORY.md` with the facts the lane depends on.
- [ ] Fill in `governance.md`: owners, approval gates, the do-not-contact
      (scrub) rule, and where the kill switch is.
- [ ] Test the kill switch. Actually pull it. A kill switch that has never
      been pulled is a decoration.
- [ ] Run `rollout-pack check .` — every rule must PASS before go-live.
- [ ] Owner signs the governance sheet.

## Week 1 — pilot with a human in the loop

- [ ] The AI employee drafts; the human approves every single send,
      publish, or payment. No exceptions while trust is being earned.
- [ ] Correct mistakes in memory, not just in the draft. Log each
      correction in `MEMORY.md` the same day.
- [ ] Keep a simple log: tasks done, minutes a human would have spent,
      errors caught. This log is your evidence at the month review.
- [ ] End of week: owner reviews the log and the corrections. Decide what
      the lane may do next week that it could not do this week — in
      writing, on the one-pager.

## First month — earn scope, then add the next lane

- [ ] Weekly: re-run `rollout-pack check .` after any one-pager or
      governance change.
- [ ] Review the scrub list handling: confirm zero outreach to anyone on
      the do-not-contact list.
- [ ] Month review: compare the time log against the hours the lane was
      meant to save. Keep, shrink, or stop the lane based on the numbers.
- [ ] Only now consider a second lane — and it gets its own one-pager, its
      own owner, and its own day one.
