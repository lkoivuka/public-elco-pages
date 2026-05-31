# public-elco-pages

Public support, privacy, and terms pages for ELCO's iOS apps, served via
GitHub Pages. **This repo is public** (the `public-` prefix is the reminder) —
never put anything sensitive here.

Live: https://lkoivuka.github.io/public-elco-pages/

## What's published

One shared site, one section per app. **Only apps that have a folder under
`apps/` are published** — nothing else. Currently:

| App | Support | Privacy | Terms |
|-----|---------|---------|-------|
| Everglades Topo | `/evergladestopo/` | `/evergladestopo/privacy/` | `/evergladestopo/terms/` |
| Hush | `/hush/` | `/hush/privacy/` | `/hush/terms/` |

Each app's pages reflect **that app's actual data practices** — they are not a
shared boilerplate policy.

## Add an app

1. `apps/<slug>/meta.json` — `{ "name", "tagline", "icon" }`
2. `apps/<slug>/privacy.md`, `terms.md`, `support.md` (first line `# Title`)
3. `assets/<slug>-icon.png`
4. `python3 build.py` (needs `pip install markdown`)
5. Review the diff, then `git commit && git push` — Pages redeploys in ~1 min.

Do **not** add an app here until its owner has explicitly approved publishing.

## Before every publish — hard rules

- Run the forbidden-vocabulary scan (see the launch runbook in the app
  monorepo, `docs/APP_STORE_LAUNCH_RUNBOOK.md`). Nothing about unrelated apps
  or internal projects may appear here.
- Confirm only approved apps are present under `apps/`.
- No secrets, no placeholders (`example.com`, `TODO`), no internal notes.

## Support contact

All apps route support to `elco.apps.team+app.support@gmail.com`.
