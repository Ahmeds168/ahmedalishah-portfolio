# Ahmed Ali Shah — Portfolio Site

Personal portfolio and resume site for Syed Ahmed Ali Shah.

Built with **Astro** (+ React for interactive islands, Tailwind CSS for the blog),
deployed on Vercel with git-based auto-deploy.

## Structure

- `src/data/resume.json` — single source of truth for experience, skills,
  projects, education, and certificates. Both the site pages and the resume
  PDF generator read from this file — update it once, everything stays in sync.
- `src/content/blog/*.md` — blog posts as Markdown content collection entries.
- `src/pages/` — Astro pages (file-based routing).
- `src/layouts/Layout.astro` — shared nav/footer/head, used by every page.
- `src/components/BlogFilters.tsx` — React island for the blog search/filter.
- `api/resume.py` — Vercel Python serverless function that generates the
  resume PDF on demand from `src/data/resume.json`.

## Local development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```
