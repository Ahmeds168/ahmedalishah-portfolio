/**
 * Single source of truth for blog categories.
 *
 * Add a new topic by adding one entry here — the content schema, the category
 * filter UI and the per-article label/colour all derive from this map, so no
 * other file needs editing.
 *
 * `label` is what readers see. `color` is the accent used for the category chip.
 */
export const CATEGORIES = {
  blockchain:        { label: 'Blockchain & Cryptography', color: '#FF5CA8' },
  solidity:          { label: 'Solidity',                  color: '#FF5CA8' },
  foundry:           { label: 'Foundry & Tooling',         color: '#F0883E' },
  'web-development': { label: 'Web Development',           color: '#2563EB' },
  javascript:        { label: 'JavaScript',                color: '#E3B341' },
  react:             { label: 'React',                     color: '#38BDF8' },
  nodejs:            { label: 'Node.js',                   color: '#3FB950' },
  python:            { label: 'Python',                    color: '#4B8BBE' },
  databases:         { label: 'Databases & SQL',           color: '#8B5CF6' },
  ai:                { label: 'AI & Applied Engineering',  color: '#5B8CFF' },
  security:          { label: 'Security',                  color: '#F85149' },
  systems:           { label: 'Systems & Infrastructure',  color: '#5B8CFF' },
  devops:            { label: 'DevOps & Deployment',       color: '#3FB950' },
  ojs:               { label: 'Open Journal Systems',      color: '#0EA5E9' },
} as const;

export type CategorySlug = keyof typeof CATEGORIES;

/** Tuple of valid slugs, for the Zod enum in content.config.ts. */
export const CATEGORY_SLUGS = Object.keys(CATEGORIES) as [CategorySlug, ...CategorySlug[]];

/** Reader-facing label for a category, with a safe fallback. */
export function categoryLabel(slug: string): string {
  return CATEGORIES[slug as CategorySlug]?.label ?? slug;
}

/** Accent colour for a category, with a safe fallback. */
export function categoryColor(slug: string): string {
  return CATEGORIES[slug as CategorySlug]?.color ?? '#2563EB';
}
