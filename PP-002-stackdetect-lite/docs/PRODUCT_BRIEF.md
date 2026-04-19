# StackDetect Lite — Product Brief

## What it does
A best-effort, browser-run tech stack detector:
- Input: URL (proxy fetch) or pasted HTML/JS
- Output: categorized detections + confidence score + “why we think this” samples

This is the *Lite* (static) version. The paid product is a server-side crawler that avoids CORS and can scan at scale.

## Who it’s for
- Agencies doing quick teardown of prospects
- Founders validating competitor stacks
- Sales teams wanting personalization cues (e.g., Stripe? HubSpot? OpenAI?)

## Why now
The stack signal surface has shifted: AI vendors, analytics, auth, and infra are central to product capability and pricing.

## MVP scope
Static single-page app. Detection based on regex patterns. No data retention beyond local storage.

## Pricing strategy
- Free: paste-mode scans, limited categories
- Pro £29/mo: crawler, exports, monitoring
- Team £99/mo: workspaces + API

## Risks
- Accuracy: static-only is limited. Must label as best-effort.
- Legal: avoid scraping private pages; respect robots for server version.
