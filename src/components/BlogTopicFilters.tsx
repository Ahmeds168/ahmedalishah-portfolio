import { useState, useMemo, useEffect } from 'react';

interface Post {
  slug: string;
  title: string;
  category: string;
  categoryLabel: string;
  categoryColor: string;
}

interface Props {
  posts: Post[];
}

/** Read ?topic= from the address bar, ignoring values that match no post. */
function topicFromUrl(valid: Set<string>): string {
  if (typeof window === 'undefined') return 'all';
  const t = new URLSearchParams(window.location.search).get('topic') || 'all';
  return valid.has(t) ? t : 'all';
}

export default function BlogTopicFilters({ posts }: Props) {
  // Derive chips from the posts actually present, so adding a category to
  // src/data/categories.ts (or recategorising a post) needs no edit here.
  const { counts, order, labels, colors } = useMemo(() => {
    const c: Record<string, number> = { all: posts.length };
    const l: Record<string, string> = {};
    const col: Record<string, string> = {};
    for (const p of posts) {
      c[p.category] = (c[p.category] || 0) + 1;
      l[p.category] = p.categoryLabel;
      col[p.category] = p.categoryColor;
    }
    const o = Object.keys(l).sort((a, b) => (c[b] - c[a]) || a.localeCompare(b));
    return { counts: c, order: o, labels: l, colors: col };
  }, [posts]);

  const valid = useMemo(() => new Set(['all', ...order]), [order]);
  const [active, setActive] = useState('all');

  // On load, pick up a topic from the URL (e.g. /blog?topic=security).
  useEffect(() => { setActive(topicFromUrl(valid)); }, [valid]);

  function select(topic: string) {
    setActive(topic);
    document.documentElement.dataset.blogTag = topic;
    // Keep the choice in the address so a filtered list can be shared or bookmarked.
    const url = new URL(window.location.href);
    if (topic === 'all') url.searchParams.delete('topic'); else url.searchParams.set('topic', topic);
    window.history.replaceState(null, '', url);
    window.dispatchEvent(new CustomEvent('blogfilter:change'));
  }

  const chip = 'shrink-0 inline-flex items-center gap-2 px-3.5 py-[7px] rounded-full border font-body font-medium text-[14px] leading-5 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent';
  const on = 'bg-ink border-ink text-white';
  const off = 'bg-card border-[#E2E8F0] text-[#334155] hover:border-[#94A3B8]';

  return (
    <div
      role="group"
      aria-label="Filter posts by topic"
      className="flex gap-2 overflow-x-auto sm:flex-wrap sm:overflow-visible pb-1 -mb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
    >
      <button type="button" aria-pressed={active === 'all'} aria-label={`All topics, ${counts.all} posts`} onClick={() => select('all')} className={`${chip} ${active === 'all' ? on : off}`}>
        All <span className={`text-[12.5px] ${active === 'all' ? 'text-[#CBD5E1]' : 'text-[#64748B]'}`}>{counts.all}</span>
      </button>
      {order.map((cat) => (
        <button key={cat} type="button" aria-pressed={active === cat} aria-label={`${labels[cat] ?? cat}, ${counts[cat]} post${counts[cat] === 1 ? '' : 's'}`} onClick={() => select(cat)} className={`${chip} ${active === cat ? on : off}`}>
          <span aria-hidden="true" className="w-[7px] h-[7px] rounded-full" style={{ background: colors[cat] }}></span>
          {labels[cat] ?? cat}
          <span className={`text-[12.5px] ${active === cat ? 'text-[#CBD5E1]' : 'text-[#64748B]'}`}>{counts[cat]}</span>
        </button>
      ))}
    </div>
  );
}
