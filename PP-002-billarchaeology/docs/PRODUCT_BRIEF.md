# Product brief — BillArchaeology

BillArchaeology is a browser-only audit workspace for SaaS/RevOps teams whose legacy contracts do not map cleanly to billing systems. It turns one messy billing clause into a clause clarity score, expected-vs-actual invoice variance, finance/legal questions, CSV exports, and a manual audit order payload.

## Target customer

- B2B SaaS finance, RevOps, and operations leads.
- Fractional CFO / RevOps consultants reviewing client billing hygiene.
- Teams with custom legacy contracts, manual billing reviews, or unclear renewals/overages.

## Core workflow

1. Paste a contract billing clause.
2. Enter billable units, expected unit price, minimum, discount, and actual invoice amount.
3. Get variance math and missing-term flags.
4. Save audits locally, export CSV, copy a report, or package a £49 manual audit request.
5. Capture interested leads locally until a real email/CRM integration is connected.

## Pricing model

- Free checker: local browser audit and CSV export.
- £49 manual audit: one clause reviewed by a human with billing-rule map and questions.
- £99/mo team workspace: shared clause library, audit history, templates, approval trail, and billing-system exports.

## Competitive advantage

BillArchaeology is narrower than generic contract analysis tools: it focuses only on the expensive gap between contract wording and recurring invoices. That makes it easier to sell to RevOps/fractional CFO buyers as a fast revenue-leak check instead of a large legal-tech rollout.

## Current MVP status

Static, self-contained `index.html`; no external CDN dependencies. Data is stored in localStorage. Payment link is a local setting so Tony can drop in a real Stripe Payment Link when ready.
