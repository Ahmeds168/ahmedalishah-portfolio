/**
 * Podcast media URL resolution.
 *
 * Audio files are NOT stored in this repo or in `public/` — they live in the
 * `ahmed-podcasts` Cloudflare R2 bucket and are served over HTTPS, either via
 * R2's public bucket access or (once configured) a custom domain such as
 * media.ahmedalishah.com.
 *
 * Every episode's frontmatter stores only a relative `audioPath` (e.g.
 * "/podcasts/001-ai-agents-security/episode.mp3"). This function is the one
 * place that combines that path with the actual media host, read from the
 * PUBLIC_PODCAST_MEDIA_URL environment variable — so changing hosts (R2 dev
 * URL -> custom domain) never requires touching component or page code.
 *
 * Returns null if either the env var isn't configured yet, or the episode
 * has no audioPath — callers (AudioPlayer, JSON-LD) treat null as "no audio
 * yet" and render the honest placeholder state instead of a broken player.
 */
export function getPodcastAudioUrl(audioPath: string | null | undefined): string | null {
  if (!audioPath) return null;

  const base = import.meta.env.PUBLIC_PODCAST_MEDIA_URL;
  if (!base) return null;

  return `${base.replace(/\/$/, '')}${audioPath.startsWith('/') ? '' : '/'}${audioPath}`;
}
