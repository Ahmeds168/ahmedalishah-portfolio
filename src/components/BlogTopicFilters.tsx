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

export default function BlogTopicFilters({ posts }: Props) {
  const [activeTag, setActiveTag] = useState('all');

  // Derive chips from the posts actually present, so adding a category to
  // src/data/categories.ts (or recategorising a post) needs no edit here.
  const { counts, categoryOrder, labels } = useMemo(() => {
    const c: Record<string, number> = { all: posts.length };
    const l: Record<string, string> = {};
    for (const p of posts) {
      c[p.category] = (c[p.category] || 0) + 1;
      l[p.category] = p.categoryLabel;
    }
    const order = Object.keys(l).sort((a, b) => (c[b] - c[a]) || a.localeCompare(b));
    return { counts: c, categoryOrder: order, labels: l };
  }, [posts]);

  function select(tag: string) {
    setActiveTag(tag);
    document.documentElement.dataset.blogTag = tag;
    window.dispatchEvent(new CustomEvent('blogfilter:change'));
  }

  return (
    <div className="bg-card p-6 rounded-xl border border-line flex flex-col gap-3">
      <div className="flex items-center justify-between pb-1">
        <span className="font-mono text-[11px] text-muted uppercase tracking-wider">Filter by topic</span>
        <span className="font-mono text-[11px] text-muted">{categoryOrder.length} topics</span>
      </div>
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => select('all')}
          className={`px-3 py-1 rounded-full font-mono text-[11px] transition-colors ${
            activeTag === 'all' ? 'bg-accent text-white font-medium' : 'bg-subtle border border-line text-ink hover:border-accent'
          }`}
        >
          All <span className="opacity-70">{String(counts.all ?? 0).padStart(2, '0')}</span>
        </button>
        {categoryOrder.map((cat) => (
          <button
            key={cat}
            type="button"
            onClick={() => select(cat)}
            className={`px-3 py-1 rounded-full font-mono text-[11px] flex items-center gap-1 transition-colors ${
              activeTag === cat ? 'bg-accent text-white font-medium' : 'bg-subtle border border-line text-ink hover:border-accent'
            }`}
          >
            <span>{labels[cat] ?? cat}</span>
            <span className="opacity-70">{String(counts[cat] ?? 0).padStart(2, '0')}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
