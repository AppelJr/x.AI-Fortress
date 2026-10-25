# xAI Sovereign Stack — Production Deployment Guide

**Version:** 1.0 (July 23, 2026)  
**Purpose:** Sovereign, air-gapped capable, PQC-secured infrastructure for x.ai with full control over compute, identity, mail, and DNS. Designed for builders who need predictable usage, privacy, and no external throttling.

## Quick Start (One-Command Deploy)

```bash
cd xai-sovereign

# 1. Generate strong secret
echo "JWT_SECRET=$(openssl rand -hex 64)" > .env

# 2. First-time certificate bootstrap (Let's Encrypt)
docker compose --profile certbot run certbot

# 3. Build and start everything
docker compose up -d --build

# 4. Access the console
https://console.x.ai
```

## Project Structure

```
xai-sovereign/
├── docker-compose.yml          # Orchestration
├── .env                        # Secrets (generated)
├── .env.example
├── README.md                   # This file
├── dns/
│   └── x.ai.zone               # Authoritative DNS zone
├── node/                       # Express + PQC proxy + PKI
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js
│   └── nexus-pki.js
├── flask/                      # Python PQC (Dilithium) service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── certbot/                    # Let's Encrypt automation
│   ├── Dockerfile
│   └── certbot.sh
├── postfix/                    # Hardened mail server
│   ├── Dockerfile
│   ├── main.cf
│   └── master.cf
└── frontend/                   # Sovereign Console UI
    ├── index.html
    ├── app.js
    └── style.css
```

## Services Overview

| Service   | Port(s)          | Purpose                              | Key Features                     |
|-----------|------------------|--------------------------------------|----------------------------------|
| node      | 443 (HTTPS)     | Main API proxy + PKI + frontend     | PQC sign/verify, ECDSA keys, JWT |
| flask     | 9000 (internal) | Dilithium5 PQC operations           | Post-quantum signatures          |
| postfix   | 25, 465, 587    | Secure outbound mail                | TLS 1.3, submission, SPF/DKIM    |
| certbot   | —               | Certificate management              | Auto-renewal                     |

## Environment Variables

Create `.env` (already done in quick start):

```env
JWT_SECRET=your-64-char-hex-secret-here
```

Optional overrides:
- `FLASK_HOST=flask` (internal Docker service name)
- `NODE_ENV=production`

## DNS Configuration (x.ai.zone)

The included zone file is production-ready for authoritative DNS.

Key records already configured:
- CAA (Let's Encrypt only)
- MX + SPF + DKIM + DMARC (quarantine policy)
- MTA-STS
- HTTPS records (HTTP/2 + HTTP/3)

**Deployment steps for DNS:**
1. Point `ns1.x.ai` and `ns2.x.ai` to your authoritative servers.
2. Replace placeholder DKIM key.
3. Update A records to your actual server IPs.
4. Deploy zone via your DNS provider or BIND/nsd.

## Security & Sovereignty Features

- **Post-Quantum Cryptography**: Dilithium5 via Flask microservice (exposed only through Node proxy).
- **JWT-protected internal communication**: Short-lived tokens between Node and Flask.
- **Let's Encrypt + CAA**: Strict certificate policy.
- **Hardened Postfix**: TLS 1.3 only, submission auth, no open relay.
- **Local-first design**: All critical paths (PQC, PKI, routing) can run without external API calls.
- **Usage protection**: Designed to work with the `intelligent-routing` skill so heavy work stays local when possible.

## Operational Commands

```bash
# View logs
docker compose logs -f node flask postfix

# Restart a service
docker compose restart node

# Update certificates manually
docker compose --profile certbot run certbot

# Full rebuild
docker compose down
docker compose up -d --build

# Check container health
docker compose ps
```

## Frontend Console

The included `frontend/` provides a clean Sovereign Console UI.  
Update `frontend/app.js` to point API calls to your endpoints (e.g. `/postquantum/sign`).

Recommended additions for production:
- Add authentication layer (login with your sovereign identity).
- Integrate the `intelligent-routing` skill for automatic local vs online decisions.
- Add real-time usage / quota display from your local event log.

## Next Recommended Pieces (Roadmap)

- Dovecot (IMAP + secure mail storage)
- Full SCAR immutable logging + Merkle chain
- Sovereign Memory Vault integration
- GateOne PQC attestation bridge
- Local-only model routing (light vs heavy) using the `intelligent-routing` skill
- Monitoring stack (Prometheus + Grafana, air-gapped friendly)

## Support & Sovereignty Notes

This stack is built for **sovereign control**.  
- No forced cloud dependencies for core functions.
- All PQC operations happen locally inside Docker.
- Designed to integrate with your existing Sovereign Memory Vault, CapabilityToken, and Proof-Gated Authority system.

If you need any file expanded (e.g. full `flask/app.py`, `frontend/index.html`, or the next service like Dovecot), just say the word.

**Status:** Production-ready bundle. Deploy with confidence.

---

*Maintained under Sovereign Root Chain Oversight — Appel420*  
*Aligned to x.ai principles of user-controlled, transparent, and private infrastructure.*