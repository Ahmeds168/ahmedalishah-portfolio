// @ts-check
import { defineConfig } from 'astro/config';

import vercel from '@astrojs/vercel';

import react from '@astrojs/react';

import tailwindcss from '@tailwindcss/vite';

import sitemap from '@astrojs/sitemap';
import { PODCAST_ENABLED } from './src/data/site';

// https://astro.build/config
export default defineConfig({
  site: 'https://ahmedalishah.vercel.app',
  adapter: vercel(),
  integrations: [
    react(),
    // Keep hidden sections out of the sitemap so search engines are not
    // pointed at pages visitors cannot reach.
    sitemap({ filter: (page) => PODCAST_ENABLED || !page.includes('/podcasts') }),
  ],

  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },

  build: {
    inlineStylesheets: 'always',
  },

  vite: {
    plugins: [tailwindcss()]
  }
});