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
- **Resume** — a downloadable PDF generated from the same data as the site
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
