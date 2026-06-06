// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// GitHub Pages project site: https://<user>.github.io/<repo>/
// If the repo or owner changes, update `site` and `base` accordingly.
export default defineConfig({
  site: 'https://neilq1810.github.io',
  base: '/emt_study',
  trailingSlash: 'ignore',
  integrations: [tailwind()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: { theme: 'github-light', wrap: true },
  },
});
