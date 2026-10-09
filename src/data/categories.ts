/**
 * Single source of truth for blog categories.
 *
 * Add a new topic by adding one entry here — the content schema, the category
 * filter UI and the per-article label/colour all derive from this map, so no
 * other file needs editing.
 *
 * `label` is what readers see. `color` is the accent: the chip's dot and its pale
 * background tint. `text` is a darker shade of the same hue for the chip's label,
 * chosen to reach at least 6:1 contrast on that tint (WCAG AA needs 4.5:1).
 */
export const CATEGORIES = {
  blockchain:        { label: 'Blockchain & Cryptography', color: '#FF5CA8', text: '#9D174D' },
  solidity:          { label: 'Solidity',                  color: '#FF5CA8', text: '#9D174D' },
  foundry:           { label: 'Foundry & Tooling',         color: '#F0883E', text: '#9A3412' },
  'web-development': { label: 'Web Development',           color: '#2563EB', text: '#1E40AF' },
  javascript:        { label: 'JavaScript',                color: '#E3B341', text: '#854D0E' },
  react:             { label: 'React',                     color: '#38BDF8', text: '#075985' },
  nodejs:            { label: 'Node.js',                   color: '#3FB950', text: '#166534' },
  python:            { label: 'Python',                    color: '#4B8BBE', text: '#1F4E79' },
  databases:         { label: 'Databases & SQL',           color: '#8B5CF6', text: '#5B21B6' },
  ai:                { label: 'AI & Applied Engineering',  color: '#5B8CFF', text: '#3730A3' },
  security:          { label: 'Security',                  color: '#F85149', text: '#991B1B' },
  systems:           { label: 'Systems & Infrastructure',  color: '#5B8CFF', text: '#3730A3' },
  devops:            { label: 'DevOps & Deployment',       color: '#3FB950', text: '#166534' },
  ojs:               { label: 'Open Journal Systems',      color: '#0EA5E9', text: '#075985' },
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

/** Readable label colour for a category, with a safe fallback. */
export function categoryTextColor(slug: string): string {
  return CATEGORIES[slug as CategorySlug]?.text ?? '#1E40AF';
}
