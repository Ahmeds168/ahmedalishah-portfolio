import { useState, useMemo } from 'react';

interface Post {
  slug: string;
  title: string;
  category: string;
  categoryLabel: string;
}

interface Props {
  posts: Post[];
}

const categoryOrder = ['blockchain', 'systems', 'ai'];

export default function BlogFilters({ posts }: Props) {
  const [query, setQuery] = useState('');
  const [activeTag, setActiveTag] = useState('all');

  const counts = useMemo(() => {
    const c: Record<string, number> = { all: posts.length };
    for (const p of posts) c[p.category] = (c[p.category] || 0) + 1;
    return c;
  }, [posts]);

  // Apply filters directly to the DOM cards Astro already rendered (progressive enhancement)
  useMemo(() => {
    if (typeof document === 'undefined') return;
    const q = query.trim().toLowerCase();
    document.querySelectorAll('[data-post-card]').forEach((el) => {
      const slug = el.getAttribute('data-slug') || '';
      const cat = el.getAttribute('data-category') || '';
      const title = (el.getAttribute('data-title') || '').toLowerCase();
      const matchesTag = activeTag === 'all' || cat === activeTag;
      const matchesQuery = q === '' || title.includes(q);
      (el as HTMLElement).style.display = matchesTag && matchesQuery ? '' : 'none';
    });
  }, [query, activeTag, posts]);

  return (
    <div className="flex flex-col gap-8">
      <div className="bg-card p-5 rounded-xl border border-line flex flex-col gap-3">
        <label htmlFor="post-search" className="font-mono text-[11px] text-muted2 uppercase tracking-wider">
          Search notes
        </label>
        <input
          id="post-search"
          type="text"
          placeholder="Search by title..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full bg-card2 text-paper placeholder:text-muted2 font-mono text-[13px] px-3 py-2 rounded-lg border border-line focus:outline-none focus:border-signal"
        />
      </div>

      <div className="bg-card p-6 rounded-xl border border-line flex flex-col gap-3">
        <div className="flex items-center justify-between pb-1">
          <span className="font-mono text-[11px] text-muted2 uppercase tracking-wider">Filter by topic</span>
          <span className="font-mono text-[11px] text-muted2">{categoryOrder.length} topics</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setActiveTag('all')}
            className={`px-3 py-1 rounded-full font-mono text-[11px] transition-colors ${
              activeTag === 'all' ? 'bg-signal text-ink font-medium' : 'bg-card2 border border-line text-paper hover:border-signal'
            }`}
          >
            All <span className="opacity-70">{String(counts.all ?? 0).padStart(2, '0')}</span>
          </button>
          {categoryOrder.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setActiveTag(cat)}
              className={`px-3 py-1 rounded-full font-mono text-[11px] flex items-center gap-1 transition-colors ${
                activeTag === cat ? 'bg-signal text-ink font-medium' : 'bg-card2 border border-line text-paper hover:border-signal'
              }`}
            >
              <span className="capitalize">{cat}</span>
              <span className="opacity-70">{String(counts[cat] ?? 0).padStart(2, '0')}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
