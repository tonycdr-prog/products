# DepositProof product brief

## What it does
DepositProof is a static, self-contained tenant deposit rebuttal pack builder. A UK renter enters the deposit amount, deduction claim, scheme, deadline, deduction explanation, evidence checklist, and labelled evidence rows. The tool produces a scheme-ready response pack with risk/readiness scoring, missing-evidence requests, a draft dispute letter, copy/download/print actions, and local paid-pack lead capture.

## Target customer
UK private renters facing a deposit deduction where the amount is large enough to justify a small one-off purchase, but not large or complex enough to immediately instruct a solicitor. The strongest wedge is urgent cleaning/damage deductions with weak invoices, missing inventory evidence, or unclear fair wear-and-tear reasoning.

## Pricing model
- Free: browser checker, evidence gaps, draft response, print/export.
- £15 Full Pack: polished response pack, saved evidence table, downloadable PDF/text workflow, Stripe Payment Link checkout.
- £49 Manual Review: async review checklist for high-value or messy claims during validation.

## Competitive advantage
DepositProof is faster and more focused than generic advice pages: it turns the renter’s facts into a structured pack they can paste into DPS/TDS/mydeposits or email to an agent. The MVP needs no account, no upload, no backend, and can validate paid intent with a Stripe Payment Link plus local lead capture.

## Current MVP status
Iterated 2026-05-26. Browser-usable static app with:
- Evidence checklist and add/remove evidence table.
- Deposit scheme selector and deadline warning.
- Readiness score and claim/deposit ratio.
- Scheme-ready draft response generation.
- Copy, download `.txt`, and print/PDF actions.
- Local paid lead capture and configurable Stripe Payment Link.

## Before chargeable v1
- Replace local lead storage with hosted capture/CRM or serverless endpoint.
- Add real Stripe Payment Links for £15 and £49 tiers.
- Add analytics for CTA clicks and pack-generation events.
- Add legal disclaimer review and scheme-specific wording checks.
