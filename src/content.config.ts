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
  }),
});

export const collections = { blog };
