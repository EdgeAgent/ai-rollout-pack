# The Governance Sheet

The governance sheet is signed before the first lane goes live. It is the
agreement between the business and its AI employee, and it outranks any
instruction the AI employee gets later. Short version: **a human owns every
lane, nothing leaves the business unapproved, the scrub list is absolute,
and anyone can pull the kill switch.**

## The five commitments

### 1. Every lane has one human owner

Not "the team", not "whoever is around" — one named person who approves
actions, owns corrections, and answers for the lane at review time.

### 2. Approval gates on anything that leaves the business

Sending, publishing, and paying are gated actions. Approval is per action:
a yes for one message never covers the next. If the owner is unreachable,
the action waits. The AI employee never approves its own work.

### 3. The do-not-contact (scrub) rule is absolute

Anyone who asks not to be contacted goes on the do-not-contact list — the
scrub list — and stays there. The AI employee checks the list before every
outreach action. A match means the action does not happen. The AI employee
cannot remove names; only the human owner edits the list, and the default
answer is no.

### 4. There is a kill switch, and it is tested

Every lane has one named, reachable way to stop it immediately: a paused
automation, a revoked login, a stopped schedule. Anyone on staff may pull
it. Only the lane owner may restart the lane. The kill switch is tested on
day one, before go-live — a kill switch that has never been pulled is a
decoration.

### 5. The memory folder belongs to the business

Everything the AI employee knows lives in files the business owns. If the
vendor, model, or tool changes, the folder — and everything learned —
stays with the business.

## Sign-off block

Signed before go-live, re-signed whenever a lane's scope changes.

| Role | Name | Signature | Date |
| --- | --- | --- | --- |
| Business owner |  |  |  |
| Lane owner |  |  |  |
| Kill switch tested by |  |  |  |

## The checker enforces this sheet

The `rollout-pack check` command lints a rollout folder against rules
R1–R7, which are this sheet translated into checks: owners named, gates
present, write actions gated, memory written, governance on file,
one-pager per lane. If the checker fails, the rollout is not ready — no
matter how good the demo looked.
