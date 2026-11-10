# Ntandomods INC website

Small Node server (no dependencies) that serves the site, proxies the live API demo and handles the contact form.

Environment variables (set in Render):
- `API_BASE` - URL of the Ladybug API service. Change this when the API moves; nothing else needs editing.
- `CLOUD_URL` - Ladybug Cloud URL.
- `RESEND_API_KEY`, `CONTACT_TO` - turn on the contact form (messages are emailed to CONTACT_TO). Optional `CONTACT_FROM`.

Run locally: `node server.js`

## Business card and brand kit
- `/card` - digital business card (flip, save contact, share). `/card.vcf` downloads the contact file.
- `/brand` - logos, colours, fonts, social covers, print-ready card.
- Card details come from `config/card.json`; env vars `CARD_NAME`, `CARD_TITLE`, `CARD_EMAIL`, `CARD_PHONE`, `CARD_WHATSAPP` override it.
- To regenerate cards and social images after editing `config/card.json`: `uv run --with cairosvg --with pillow python3 scripts/build-assets.py` (needs `qrencode` and the Sora and Figtree fonts).
- `/api/status` reports whether Ladybug API is up (used by the footer badge).
