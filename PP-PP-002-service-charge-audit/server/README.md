# ServiceChargeSense — Waitlist endpoint (Node)

This static MVP can submit emails to a **real endpoint** if you run/deploy the included Node server.

## Run locally

```bash
cd output/builds/PP-PP-002-service-charge-audit
node server/waitlist-server.js
# listens on http://0.0.0.0:8787
```

Then open `index.html` and set:

- **Waitlist endpoint URL** → `http://localhost:8787/api/waitlist`

(If you’re opening the HTML as a `file://` URL, some browsers may block requests to `http://localhost`. If that happens, serve the folder locally e.g. `python3 -m http.server` and open `http://localhost:8000/index.html`.)

## Deploy

This file is dependency-free; deploy it anywhere you can run Node 18+.

Environment variables:
- `PORT` (default `8787`)
- `HOST` (default `0.0.0.0`)
- `WAITLIST_ADMIN_TOKEN` (optional; enables `GET /api/waitlist` with `Authorization: Bearer <token>`)

## Endpoints

- `POST /api/waitlist`
  - JSON body:
    ```json
    {"email":"you@domain.com","name":"Alex","product":"ServiceChargeSense","source":"https://...","audit":{"prev":1800,"curr":3200,"pct":77.7}}
    ```
  - Response: `{ "ok": true }`

- `GET /api/health` → `{ ok: true, ... }`
