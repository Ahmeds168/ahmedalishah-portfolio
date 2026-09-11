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

export const collections = { blog };
