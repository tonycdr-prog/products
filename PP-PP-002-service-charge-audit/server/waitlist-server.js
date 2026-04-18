#!/usr/bin/env node
/**
 * ServiceChargeSense — minimal waitlist collector
 *
 * Purpose: give the static MVP a real endpoint you can deploy anywhere Node runs.
 * - POST /api/waitlist  (JSON)  → appends to data/waitlist.jsonl
 * - GET  /api/health            → basic health response
 * - GET  /api/waitlist          → returns entries (requires WAITLIST_ADMIN_TOKEN)
 *
 * No dependencies. Node 18+.
 */

import http from 'node:http';
import { URL, fileURLToPath } from 'node:url';
import fs from 'node:fs';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = parseInt(process.env.PORT || '8787', 10);
const HOST = process.env.HOST || '0.0.0.0';
const ADMIN_TOKEN = process.env.WAITLIST_ADMIN_TOKEN || '';

const DATA_DIR = path.join(__dirname, '..', 'data');
const OUT_PATH = path.join(DATA_DIR, 'waitlist.jsonl');

function ensureDataDir(){
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function send(res, status, obj, headers = {}){
  const body = JSON.stringify(obj);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    ...headers,
  });
  res.end(body);
}

function readBody(req, limitBytes = 200 * 1024){
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', (c) => {
      size += c.length;
      if (size > limitBytes) {
        reject(new Error('Body too large'));
        req.destroy();
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function isValidEmail(email){
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email || '').trim());
}

// Very light in-memory throttling per IP (best-effort)
const ipHits = new Map();
function tooMany(ip){
  const now = Date.now();
  const winMs = 60_000;
  const max = 30;
  const arr = ipHits.get(ip) || [];
  const recent = arr.filter((t) => now - t < winMs);
  recent.push(now);
  ipHits.set(ip, recent);
  return recent.length > max;
}

const server = http.createServer(async (req, res) => {
  // CORS: allow from anywhere; tighten once deployed on a real domain.
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const u = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const ip = (req.headers['x-forwarded-for'] || '').toString().split(',')[0].trim() || req.socket.remoteAddress || 'unknown';

  try {
    if (u.pathname === '/api/health') {
      send(res, 200, { ok: true, service: 'ServiceChargeSense waitlist', ts: new Date().toISOString() });
      return;
    }

    if (u.pathname === '/api/waitlist' && req.method === 'POST') {
      if (tooMany(ip)) {
        send(res, 429, { ok: false, error: 'rate_limited' });
        return;
      }

      const raw = await readBody(req);
      let payload;
      try {
        payload = JSON.parse(raw || '{}');
      } catch {
        send(res, 400, { ok: false, error: 'invalid_json' });
        return;
      }

      const email = (payload.email || '').toString().trim();
      const name = (payload.name || '').toString().trim();
      const product = (payload.product || 'ServiceChargeSense').toString();
      const source = (payload.source || '').toString();
      const audit = payload.audit && typeof payload.audit === 'object' ? payload.audit : null;

      if (!isValidEmail(email)) {
        send(res, 400, { ok: false, error: 'invalid_email' });
        return;
      }

      ensureDataDir();
      const entry = {
        email,
        name: name || null,
        product,
        source: source || null,
        audit,
        receivedAt: new Date().toISOString(),
        ip: ip || null,
        ua: (req.headers['user-agent'] || '').toString().slice(0, 400) || null,
      };

      fs.appendFileSync(OUT_PATH, JSON.stringify(entry) + '\n', 'utf8');
      send(res, 200, { ok: true });
      return;
    }

    if (u.pathname === '/api/waitlist' && req.method === 'GET') {
      const auth = (req.headers.authorization || '').toString();
      const token = auth.startsWith('Bearer ') ? auth.slice('Bearer '.length) : '';
      if (!ADMIN_TOKEN || token !== ADMIN_TOKEN) {
        send(res, 403, { ok: false, error: 'forbidden' });
        return;
      }

      ensureDataDir();
      if (!fs.existsSync(OUT_PATH)) {
        send(res, 200, { ok: true, count: 0, entries: [] });
        return;
      }

      const lines = fs.readFileSync(OUT_PATH, 'utf8').split('\n').filter(Boolean);
      const entries = lines.slice(-500).map((l) => {
        try { return JSON.parse(l); } catch { return null; }
      }).filter(Boolean);

      send(res, 200, { ok: true, count: lines.length, entries });
      return;
    }

    send(res, 404, { ok: false, error: 'not_found' });
  } catch (err) {
    send(res, 500, { ok: false, error: 'server_error', message: String(err?.message || err) });
  }
});

server.listen(PORT, HOST, () => {
  console.log(`ServiceChargeSense waitlist server listening on http://${HOST}:${PORT}`);
  console.log('POST /api/waitlist  (JSON: {email,name,product,source,audit})');
  console.log('GET  /api/health');
});
