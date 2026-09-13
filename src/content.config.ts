import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    category: z.enum(['blockchain', 'systems', 'ai']),
    categoryLabel: z.string(),
    categoryColor: z.string(),
    banner: z.string(),
    metaLine: z.string(),
    pubDate: z.coerce.date(),
    order: z.number(),
    stack: z.array(z.string()).optional(),
    pullQuote: z.string().optional(),
    codeSnippet: z.object({
      filename: z.string(),
      code: z.string(),
    }).optional(),
  }),
});

const podcast = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/podcast' }),
  schema: z.object({
    title: z.string(),
    shortDescription: z.string(),
    description: z.string(),
    episodeNumber: z.number(),
    date: z.coerce.date(),
    duration: z.string(),          // e.g. "18 min" — display string
    durationSeconds: z.number().optional(), // for schema.org ISO 8601 duration
    audioPath: z.string().nullable().default(null), // e.g. "/podcasts/001-ai-agents-security/episode.mp3" — resolved against PUBLIC_PODCAST_MEDIA_URL
    topics: z.array(z.string()),
    featured: z.boolean().default(false),
    inThisEpisode: z.array(z.string()),
    timestamps: z.array(z.object({ time: z.string(), label: z.string() })),
    resources: z.array(z.object({ label: z.string(), url: z.string() })).optional(),
    relatedArticles: z.array(z.string()).optional(), // blog post slugs
    relatedEpisodes: z.array(z.string()).optional(), // podcast slugs
    seoTitle: z.string().optional(),
    seoDescription: z.string().optional(),
  }),
});

export const collections = { blog, podcast };
