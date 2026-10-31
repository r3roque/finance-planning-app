# Finance Planning

Budget planning, expense tracking, paychecks and a Puerto Rico income tax estimate, served at **https://financeplanning.app**.

- Hosting: Cloudflare Pages, serving the `public/` folder as static files. There's no build step on Cloudflare.
- Accounts and data: Supabase. Sign in with email and password, with a confirmation email; Google sign-in can be turned on later.
- Every person's data sits in two tables (`user_settings` and `expenses`) protected by row level security, so a signed-in person can only read and write their own rows.

## Layout

| Path | What it is |
|---|---|
| `src/app.html` | The app itself (markup, styles, logic). Edit this. |
| `build.py` | Wraps `src/app.html` into `public/index.html` with the website head (Supabase config, manifest, service worker). Run `python3 build.py` after editing. |
| `public/` | What Cloudflare serves: `index.html`, service worker, manifest, icons, `_headers` (security headers), and the Supabase client library (`vendor/`, MIT licensed). |
| `supabase/schema.sql` | Database tables, privacy rules, and the delete-account function. Run once in the Supabase SQL editor. |

## One-time setup

### Supabase
1. **SQL Editor → New query**: paste all of `supabase/schema.sql` and click **Run**.
2. **Authentication → Sign In / Providers → Email**: keep **Confirm email** on.
3. **Authentication → URL Configuration**:
   - Site URL: `https://financeplanning.app`
   - Redirect URLs: add `https://financeplanning.app/**` and your Pages preview address, e.g. `https://finance-planning-app.pages.dev/**`.
4. Before real users arrive: **Authentication → Emails → SMTP Settings**, connect an email provider (e.g. Resend or Postmark). The built-in sender is rate-limited and meant for testing.

### Cloudflare Pages
1. **Workers & Pages → Create → Pages → Connect to Git**, pick this repository.
2. Framework preset: **None**. Build command: *(leave empty)*. Build output directory: **`public`**.
3. After the first deploy: **Custom domains → Set up a custom domain → `financeplanning.app`**. Optionally add `www.financeplanning.app` and redirect it to the main domain.

Every push to `main` deploys automatically.

## Google sign-in
1. Google Cloud Console → **APIs & Services → OAuth consent screen**: app name "Finance Planning", your support email, authorized domain `financeplanning.app`. Publish the app when ready for everyone.
2. **Credentials → Create credentials → OAuth client ID** → Web application.
   - Authorized JavaScript origins: `https://financeplanning.app`
   - Authorized redirect URI: `https://pqrkysbqufrxvqvxnibc.supabase.co/auth/v1/callback`
3. Supabase → **Authentication → Sign In / Providers → Google**: paste the client ID and secret, enable, save.
4. Supabase → **Authentication → Sign In / Providers**: turn on **Allow manual linking** so people can connect Google from Settings → Account.

Accounts with the same confirmed email are linked automatically; a different Google email can be connected from Settings → Account.

## Passkeys (beta in Supabase)
Supabase → **Authentication → Passkeys** → enable, then:
- Relying Party Display Name: `Finance Planning`
- Relying Party ID: `financeplanning.app` (don't change it later; that invalidates every passkey)
- Relying Party Origins: `https://financeplanning.app,https://www.financeplanning.app`

Passkeys work only on financeplanning.app (not the workers.dev address). People add them in Settings → Account, or from the prompt after a password sign-in.
The switches for both live in `build.py` (`google`, `passkeys`).

## Notes
- The Supabase **anon key** in `build.py` is meant to be public; the row level security rules are what keep data private. Never put the `service_role` key in this repo.
- The same `src/app.html` also runs as a Claude artifact, where it stores data in the person's Claude account instead of Supabase.
