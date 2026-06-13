// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkFigures from './src/lib/remark-figures.mjs';

// GitHub Pages project site: https://<user>.github.io/<repo>/
// If the repo or owner changes, update `site` and `base` accordingly.
const base = '/emt_study';

export default defineConfig({
  site: 'https://neilq1810.github.io',
  base,
  trailingSlash: 'ignore',
  integrations: [tailwind()],
  markdown: {
    remarkPlugins: [remarkMath, [remarkFigures, { base }]],
    rehypePlugins: [rehypeKatex],
    shikiConfig: { theme: 'github-light', wrap: true },
  },
});
