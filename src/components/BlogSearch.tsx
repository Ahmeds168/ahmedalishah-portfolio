import { useState } from 'react';

export default function BlogSearch() {
  const [query, setQuery] = useState('');

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const value = e.target.value;
    setQuery(value);
    document.documentElement.dataset.blogSearch = value;
    window.dispatchEvent(new CustomEvent('blogfilter:change'));
  }

  return (
    <div className="bg-card p-5 rounded-xl border border-line flex flex-col gap-3">
      <label htmlFor="post-search" className="font-mono text-[11px] text-muted uppercase tracking-wider">
        Search notes
      </label>
      <input
        id="post-search"
        type="text"
        placeholder="Search by title..."
        value={query}
        onChange={handleChange}
        className="w-full bg-subtle text-ink placeholder:text-muted font-mono text-[13px] px-3 py-2 rounded-lg border border-line focus:outline-none focus:border-accent"
      />
    </div>
  );
}
