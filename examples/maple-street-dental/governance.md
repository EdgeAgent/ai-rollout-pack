# Governance — Maple Street Dental (SAMPLE, fictional)

Signed before the first lane went live. This sheet outranks any later
instruction given to an AI employee.

## Lanes and owners

| Lane | Owns | Human owner |
| --- | --- | --- |
| front-desk | Bookings, reminders, first replies | Office Manager |
| faq | Patient questions from approved documents | Office Manager |
| billing-watch | Flags overdue invoices for humans | Clinic Owner |

## Approval gates

- `front-desk` may draft freely. **Sending** any message needs the Office
  Manager's approval, per message, every time.
- `faq` and `billing-watch` are read-only lanes. They produce drafts and
  flags for humans; they never contact a patient.
- No lane takes payments or changes the booking system of record.

## Do-not-contact (scrub) rule

- Patients who ask not to receive reminders or messages go on the
  do-not-contact list (the scrub list) the same day.
- The scrub list is checked before every reminder run. A match means no
  message — and no note in the patient's file beyond "do not contact".
- Only the Clinic Owner edits the scrub list. The default answer is no.

## Kill switch

- Kill switch for all lanes: pause the clinic automations account and
  revoke the AI employee's mailbox login. Either step stops every lane.
- Tested on day one by the Office Manager; restart is the Clinic Owner's
  decision only.

## Data boundaries

- Patient information stays in the clinic's own systems. Nothing is copied
  into personal accounts or public tools.
- The memory folder is clinic property and is backed up with clinic
  records.

## Sign-off

| Role | Name | Signature | Date |
| --- | --- | --- | --- |
| Business owner | Clinic Owner | (sample) | Day 1 |
| Lane owner (front-desk, faq) | Office Manager | (sample) | Day 1 |
