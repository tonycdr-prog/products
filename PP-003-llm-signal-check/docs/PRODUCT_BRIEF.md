# LLM Signal Check — Product Brief

## What it does
A lead-gen helper that tries to detect public web signals of LLM usage.

**Two input paths:**
- **Fetch mode:** paste a list of domains → we fetch public HTML (best-effort) via a proxy
- **Paste mode (fallback):** paste raw HTML/JS/text from View Source / DevTools → we scan locally (no network)

**Output:**
- vendor hits (OpenAI/Azure OpenAI/Anthropic/Vertex/etc)
- confidence score + evidence snippets
- exportable results (CSV)

## Who it’s for
- AI consultants and agencies
- SaaS sellers targeting “AI adoption” accounts
- SDR teams doing outbound personalization

## MVP scope
Static web app; limited accuracy. The “real” product requires server-side crawling + additional data sources (job posts, GitHub org activity, subdomain enumeration, headers).

## Pricing strategy
- Free: manual scan (fetch + paste modes)
- Signals Pro £49/mo: bulk scanning, export, job post monitoring
- Agency £199/mo: teams + API

## Competitive advantage
Most quick “detectors” fail when a site blocks crawling. The paste-mode fallback lets a human still validate signals in ~60 seconds by copying a page response/body and scanning locally.

## Key risks
- False positives/negatives: must be labeled.
- Data source fragility: proxies can be blocked (mitigated by paste mode).
