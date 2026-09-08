# Banking Reform Tracker

A self-hosted, evidence-first public portal tracking the configurable status of a five-day banking week in India. It does **not** assume implementation. The default `2024-09-04T10:00:00+05:30` is labelled a configured reference date until an administrator records a verified official source.

## Quick start (Node 20+)

```bash
cp .env.example .env
# Set a unique JWT_SECRET, ADMIN_EMAIL and ADMIN_PASSWORD in .env
npm install
npm run seed
npm start
```

Open <http://localhost:3000>. If admin environment variables are omitted, the server prints one strong one-time password to its local console and flags the account for a password change. Never expose that log. The SQLite database is `data/banking-reform-tracker.db`.

Development startup monitoring is opt-in with `RUN_STARTUP_SCRAPER=true`; production schedules monitoring daily at 02:00 IST. New discoveries and generated drafts are **always pending review**. Configured HTML sources are disabled until an operator has manually confirmed their robots policy and stable selectors. The monitor uses public metadata only, throttled execution, ordinary HTTP, a descriptive user agent, timeouts, and no access-control bypass.

## Docker Compose

```bash
cp .env.example .env
# edit secrets; for production set APP_ORIGIN=https://your-host
docker compose up --build -d
docker compose logs -f tracker
```

The named `tracker-data` volume persists SQLite. For a VPS, install Docker, clone/copy the project, configure `.env`, place it behind an HTTPS reverse proxy, and run the commands above. The app trusts one proxy hop and redirects forwarded HTTP requests in production. Render/Railway-style hosts work with the Dockerfile only when `/app/data` is mounted to persistent storage; configure the same environment values and health-check `/api/timer`.

## Operations

```bash
# test and lint
npm run lint && npm test
# external system-cron alternative (do not use in addition to built-in schedule)
./cron-job.sh
# backup while stopped, or after SQLite backup API tooling
cp data/banking-reform-tracker.db backups/tracker-$(date +%F).db
# restore while stopped
cp backups/tracker-YYYY-MM-DD.db data/banking-reform-tracker.db
```

Update the generated localhost URLs in `sitemap.xml` and `robots.txt` for the deployed origin. Seed records are deliberately prominent samples; remove or archive them and enter verified information before public publishing. Admin approval, timer confirmation, tips, first-party page counts, logs, RSS, and CSV remain local.

## Security model

JWTs are short-lived HttpOnly, SameSite cookies (Secure in production). State changes require a matching CSRF header/cookie token. Login, tips, APIs, and manual scraping are rate limited. Helmet/CSP, restricted CORS, bounded bodies, parameterized SQL, generic authentication errors, and text-only DOM rendering are enabled. Set a unique 32+ character `JWT_SECRET`. Rotate credentials and back up SQLite securely. The local account is intentionally independent of Google or any hosted identity service.

## Source monitoring and optional adapters

`config.json` contains public source registry candidates and transparent keywords. Enable a source only after confirming current terms and robots rules; inaccessible sources are logged and skipped. Full copyrighted articles are never copied. Mock fixtures in tests demonstrate the workflow offline.

NewsAPI, X/Twitter, email delivery, hosted push, social auto-posting, and third-party analytics are intentionally not configured because they require accounts, credentials, or providers. Optional adapters can later implement a small `discover(): Item[]` interface and pass metadata to `runScraper`; keep them disabled by default and store credentials only in environment variables. Browser Notification API opt-in can be added client-side for same-browser notifications; RSS and the in-app approved updates view require no provider.

## API and deployment checklist

See `openapi.yaml`. Before production: set secrets and canonical origin; seed then replace/archive samples; verify sources; mount persistent storage; configure HTTPS/backups; log in locally; confirm timer remains **Monitoring**; and record an implementation date plus official URL only after human verification. No deployment or external account is performed by this repository.
