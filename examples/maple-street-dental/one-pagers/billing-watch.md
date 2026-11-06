# One-Pager — billing-watch (Maple Street Dental — SAMPLE, fictional)

## The lane

- **Lane name:** billing-watch
- **Owns:** Flags overdue invoices for human review; never contacts patients about billing
- **Human owner:** Clinic Owner

## What it does

- Reads the invoice list on a schedule
- Flags anything overdue past the clinic's threshold into a review list
  for the Clinic Owner

## Tools it may use

- read
- flag

## Needs human approval for

- Nothing leaves the business from this lane — it is read-only; every
  follow-up is a human's job

## It never

- Writes to a patient about money, ever
- Changes an invoice, a balance, or a payment record
- Shares billing details outside the clinic's own systems

## Where its memory lives

`memory/MEMORY.md` — the billing-watch note (flag only, never contact).

## Escalation

Disputed or unusual invoices go straight to the Clinic Owner's list,
flagged, untouched.
