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

export default function BlogTopicFilters({ posts }: Props) {
  const [activeTag, setActiveTag] = useState('all');

  const counts = useMemo(() => {
    const c: Record<string, number> = { all: posts.length };
    for (const p of posts) c[p.category] = (c[p.category] || 0) + 1;
    return c;
  }, [posts]);

  function select(tag: string) {
    setActiveTag(tag);
    document.documentElement.dataset.blogTag = tag;
    window.dispatchEvent(new CustomEvent('blogfilter:change'));
  }

  return (
    <div className="bg-card p-6 rounded-xl border border-line flex flex-col gap-3">
      <div className="flex items-center justify-between pb-1">
        <span className="font-mono text-[11px] text-muted2 uppercase tracking-wider">Filter by topic</span>
        <span className="font-mono text-[11px] text-muted2">{categoryOrder.length} topics</span>
      </div>
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => select('all')}
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
            onClick={() => select(cat)}
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
  );
}
