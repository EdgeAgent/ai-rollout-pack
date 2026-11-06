# Case Study — The Pattern Running in Production

A sanitized worked example, from the author's own systems. Private details
(clients, people, revenue) are removed; the structure is exactly as built.
Two systems, one pattern: **lanes with owners, gates on anything that
leaves, memory in files, and a hard stop that code — not good intentions —
enforces.**

## System 1: "Hermes" — a governed lead pipeline

A lead-generation pipeline that finds businesses, qualifies them, and runs
outreach. It is organised the way this pack prescribes:

- **A router plus worker lanes.** One component routes work; worker lanes
  each own a single job — discovery, qualification, drafting, sending.
  No lane borrows another lane's job, so when something is wrong, it is
  obvious which lane did it.
- **Dedup before anything else.** The same business is never contacted
  twice by accident. Deduplication is a gate in the pipeline, not a
  cleanup chore after a mistake.
- **A hard do-not-contact list, enforced in code.** Anyone who opts out,
  complains, or is blocked goes on the list permanently, and the send path
  checks the list before every send. The rule does not depend on an
  operator remembering it — the code refuses.
- **A governed send cap: 50 per day.** Volume is a policy decision, set in
  configuration, not a mood. The cap protects deliverability and forces
  quality over quantity.
- **Human approval before sends.** Batches are reviewed by a human before
  anything leaves. The pipeline drafts and prepares; a person says go.

What the pack took from Hermes: rules R3 and R4 (every acting lane is
gated; write actions are gated by name) and the scrub rule in the
governance sheet are this pipeline's scar tissue, written down as
templates so the next rollout starts with them instead of earning them.

## System 2: "Clockwork" — an AI employee framework

A framework for an AI employee that works a recurring job:

- **Clock-in, every run.** The employee starts each session by gathering
  context — its memory file, the relevant playbook, its schedule — before
  it acts. Nothing is assumed to carry over from last time, because
  nothing does; the context is re-read from files the business owns.
- **Skills are written instructions.** Each capability is a document the
  employee follows, the way a one-pager describes a lane: what the job is,
  what good looks like, what never to do.
- **An approval gate before execution.** Prepared work waits for a human
  yes before it runs. After execution, the employee checks its own output
  and writes what it learned back to memory.
- **Memory is a file, not a feature.** Everything the employee knows lives
  in plain files. Replacing the model or the tool loses nothing, because
  the knowledge was never inside either.

What the pack took from Clockwork: the memory folder structure, the
staff guide's correction rule ("fix the source, not just the output"),
and the checklist's insistence that scope is earned from a clean log.

## The point of the case study

None of this required a platform, a vendor, or a research lab. It required
deciding — in writing, in advance — what each lane owns, what needs a
human yes, what is never allowed, and where the memory lives. That is the
whole method of this pack, and it is running today.
