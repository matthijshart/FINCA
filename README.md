# Finca Corazón

This project serves a static website with a small backend to send contact form emails.

## Setup

1. Install the dependencies defined in `package.json`:

```bash
npm install
```

2. Configure the SMTP credentials via environment variables before starting the server:

- `SMTP_HOST`
- `SMTP_PORT` (usually `587`)
- `SMTP_SECURE` (`true` or `false`)
- `SMTP_USER`
- `SMTP_PASS`

3. Start the Node server:

```bash
node server.js
```

The server listens on port `3000` by default and serves `index.html`. The contact form will post to `/send-mail` and forward the message to `matthijsthart@icloud.com`.

### Alternative Python server

If installing Node packages isn't possible, run the lightweight Python server instead:

```bash
python3 server.py
```

This uses only the Python standard library to handle `/send-mail` requests and send the email via SMTP.

