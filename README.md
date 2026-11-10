# Ntandomods INC website

Small Node server (no dependencies) that serves the site, proxies the live API demo and handles the contact form.

Environment variables (set in Render):
- `API_BASE` - URL of the Ladybug API service. Change this when the API moves; nothing else needs editing.
- `CLOUD_URL` - Ladybug Cloud URL.
- `RESEND_API_KEY`, `CONTACT_TO` - turn on the contact form (messages are emailed to CONTACT_TO). Optional `CONTACT_FROM`.

Run locally: `node server.js`
