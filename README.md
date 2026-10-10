# Syed Ahmed Ali Shah — Portfolio

Personal portfolio, technical blog and resume site.
Live at **[ahmedalishah.vercel.app](https://ahmedalishah.vercel.app)**.

Built with [Astro](https://astro.build), React islands for the interactive parts,
and Tailwind CSS. Statically rendered and deployed on Vercel with Git-based
auto-deploy from `main`.

## What's in it

- **Projects** — portfolio cards plus full case-study pages
- **Blog** — technical articles on Foundry, Solidity, OJS administration and applied AI
- **Services** — service pages for full-stack development, Python automation,
  OJS support, Solidity/Foundry development and AI integration
- **Topic hubs** — `/foundry`, `/solidity`, `/ojs`, `/ai` group related articles
- **Resume** — a PDF generated from the same data as the site, downloadable with an access key
- **RSS** — feed of all articles at `/rss.xml`

## Structure

```
src/
  data/
    resume.json       single source of truth: experience, skills, projects,
                      education, certificates — read by the site AND the PDF
    services.json     service page content
    categories.ts     blog categories (slug, label, colour) in one place
    site.ts           feature flags
  content/
    blog/             articles as Markdown
    podcast/          podcast episodes as Markdown
  components/         shared components (Navbar, Footer, ProjectCard, ...)
  layouts/Layout.astro  shared <head>, nav and footer for every page
  pages/              file-based routing
api/
  resume.py           Vercel Python function that renders the resume PDF
scripts/              publishing helpers (see below)
```

Interactive components are React (`BlogSearch.tsx`, `BlogTopicFilters.tsx`).
Everything else ships as static HTML with no client-side JavaScript.

## Editing content

| To change... | Edit |
|---|---|
| Experience, projects, skills, certificates | `src/data/resume.json` |
| Which projects appear on the homepage | `featured` / `homepageOrder` in `resume.json` |
| A blog post | `src/content/blog/<slug>.md` |
| Blog categories | `src/data/categories.ts` |
| Service pages | `src/data/services.json` |

Changes to `resume.json` update both the site and the downloadable PDF.

### Publishing a blog post

Every post needs its own share image, or LinkedIn and X show a blank card or
fall back to the profile photo (and then cache that).

1. Write `src/content/blog/<slug>.md` and its banner in `public/images/`.
2. Generate the share image **before the first push**:
   `python3 scripts/gen-og.py <slug> "<KICKER>" "<title>" "<accent-hex>"`
   (writes `public/images/og/<slug>.png`, 1200×630).
3. Build and check there is no `[og] missing` warning, then push.
4. Before sharing, paste the URL into LinkedIn's Post Inspector to confirm the
   preview shows the share image.

If a share image is missing, the page falls back to `/images/og-image.png`.
Share image URLs carry a content fingerprint (`?v=…`), so a regenerated image
is fetched fresh by LinkedIn and X.

## Feature flags

`src/data/site.ts` controls sections that can be hidden without deleting them.
`PODCAST_ENABLED = false` hides the podcast section: nav link, episode pages,
sitemap entries and cross-links. Content is kept; set it to `true` to restore.

## Local development

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # production build into dist/
```

Requires Node 22.12 or later.

## Environment variables

| Variable | Purpose |
|---|---|
| `PUBLIC_PODCAST_MEDIA_URL` | Base URL for podcast audio on Cloudflare R2. See `.env.example`. |
| `RESUME_ACCESS_KEY` | Key required to download the resume PDF. Without a valid key, `/api/resume` redirects to the contact page. If unset, nobody can download — it fails closed. Change it in Vercel to revoke old keys. |

Set in Vercel for production and preview. Never commit a real `.env`.

## Scripts

| Script | Does |
|---|---|
| `scripts/gen-og.py` | Generates a 1200×630 Open Graph image for an article or episode |
| `scripts/new-episode.sh` | Uploads episode audio to R2 and scaffolds the episode page |
| `scripts/transcribe.sh` | Compresses audio and transcribes it with Groq Whisper |

`new-episode.sh` uses Wrangler, which requires `--remote` for R2 uploads —
without it, files go to a local simulator and never reach the bucket.

## Deployment

Pushing to `main` deploys to production. Each deployment keeps its own copy of
the Python function, so old deployments accumulate storage over time — delete
old ones periodically from the Vercel dashboard.
