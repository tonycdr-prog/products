# StackSpend Guard Product Brief

## What It Does
StackSpend Guard is a browser-only AI tooling spend audit for small teams. Users enter subscriptions, owners, monthly costs, and statuses such as Active, Trial, Duplicate, Forgotten, or Cancel. The app calculates total spend, per-user spend, budget gap, likely removable waste, and a sprawl risk score, then generates a copy-ready AI spend policy and downloadable Markdown/CSV reports.

## Target Customer
SME operators, agency owners, fractional COOs, finance leads, and dev/product managers whose AI spend is spread across ChatGPT, Claude, Cursor, image/video tools, meeting tools, and one-off usage charges.

## Pricing Model
- Free: local one-off audit, report copy, Markdown export, CSV export.
- Team Guard: £29/team/month for saved history, renewal reminders, Slack/email alerts, and policy templates.
- Agency Dashboard: £99/month for multi-client workspaces, white-labelled reports, and monthly review packs.

## Competitive Advantage
StackSpend Guard is intentionally lightweight: no procurement suite, no sales call, no card required. It creates value in under five minutes by turning messy tool spend into a practical policy and action list. The wedge is the free audit; paid conversion comes from reminders, saved history, and multi-client exports.

## Current MVP Capability
The static `index.html` now supports editable tool rows, policy checklist controls, localStorage save/reset, live metrics, generated policy text, copy-to-clipboard, Markdown download, and CSV export. All calculations run locally with vanilla JavaScript and no external dependencies.
