# ServiceChargeSense — Product Brief

## What it does
A UK-focused service charge audit helper for leaseholders.
- Takes headline service charge figures (and optional top line items)
- Produces red flags + questions to ask
- Generates a ready-to-send request letter template
- Exports report/letter as PDFs
- Captures interest via a waitlist form (local + real endpoint option)

## Who it’s for
- UK leaseholders in flats dealing with big YoY service charge changes
- People who have opaque managing agents and scattered email threads

## MVP scope (what’s in this build)
- Audit calculator (YoY delta, % change, inflation-adjusted sense-check)
- Red-flag checklist logic
- Letter generator
- PDF export (client-side)
- Waitlist capture:
  - **LocalStorage** (always available)
  - **Real endpoint** (optional): `server/waitlist-server.js` provides `POST /api/waitlist` and stores JSONL to `data/waitlist.jsonl`

## Pricing strategy
- Free checker
- £12 one-off “Report Pack” download (PDF report + letter + checklist)
- £8/mo “Pro” for multi-building tracking + reminders

## Revenue model notes
Conservative: 300 paying users * £10/mo equivalent ≈ **£3k MRR**.

## Competitive advantage (for this wedge)
- UK-specific language and outputs (not generic “budgeting”)
- Actionable: turns numbers into a short checklist + a usable letter template
- Fast: no account needed to get value

## Compliance / risk
- Not legal advice.
- Needs careful wording about statutory rights (ensure accuracy before public launch).
