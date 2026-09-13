/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
  /**
   * Base URL for podcast audio, served from the `ahmed-podcasts` Cloudflare R2
   * bucket (public bucket access or, once set up, a custom domain such as
   * media.ahmedalishah.com). No trailing slash.
   *
   * Set this in Vercel: Project Settings -> Environment Variables.
   * Locally: create a `.env` file (see `.env.example`) — never commit it.
   *
   * Episode audioPath values are resolved against this in src/lib/podcast.ts.
   */
  readonly PUBLIC_PODCAST_MEDIA_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
