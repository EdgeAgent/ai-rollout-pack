# Staff Guide — working with the AI employee at __BUSINESS_NAME__

The AI employee is a junior team member with a perfect memory for what is
written down and no memory for anything else. Treat it that way and it will
save you real time.

## How to ask it for something

- Ask the way you would ask a new hire: the task, the background, and what
  "done" looks like. "Draft a reply to this enquiry" works. "Handle it"
  does not.
- Give it the source, not your summary of the source. Paste the message,
  attach the document, name the file.
- One task per request. Bundled requests get bundled mistakes.

## How to correct it

- Correct the output, then correct the source. If a draft has the wrong
  price, fix the draft — and fix the price in its memory or one-pager, or
  the same mistake comes back tomorrow.
- Say what was wrong in plain words: "We never offer discounts on the
  phone." Corrections written into memory are permanent; corrections in
  chat are gone tomorrow.
- If it gets the same thing wrong twice, tell the lane owner. That is a
  one-pager problem, not a prompting problem.

## Where its memory lives

- Everything the AI employee knows about this business lives in the
  `memory/` folder: `MEMORY.md` holds the facts, and each lane keeps its
  own notes and playbook.
- If it is not written in the memory folder, the AI employee does not know
  it. Meeting decisions go into memory the same day.
- The folder belongs to the business. Back it up like any other business
  record.

## What it will never do

- Send, publish, or pay for anything without a human approval first.
- Contact anyone on the do-not-contact (scrub) list.
- Invent prices, policies, or availability. If it does not know, it says
  so and drafts a question for a human instead.
- Argue with a correction. The human owner's word is the final version.

## When something looks wrong

Stop the lane (the kill switch is listed in `governance.md`), then tell the
lane owner what happened. Restarting is the owner's call.
