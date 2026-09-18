import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { categoryLabel } from '../data/categories';
import resume from '../data/resume.json';

export async function GET(context) {
  const posts = (await getCollection('blog')).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  return rss({
    title: `${resume.name} — Writing`,
    description:
      'Notes on software, security, and the occasional deep dive — blockchain, Foundry, OJS administration, Python and applied AI.',
    site: context.site,
    trailingSlash: false,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.excerpt,
      pubDate: post.data.pubDate,
      link: `/blog/${post.id}`,
      categories: [post.data.categoryLabel ?? categoryLabel(post.data.category)],
      author: resume.contact.email,
    })),
    customData: '<language>en-us</language>',
  });
}
