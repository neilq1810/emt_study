import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

// Read the manuscript Markdown directly from the repo-root /book directory.
// The content lives outside the Astro app so the book remains the single
// source of truth; the site is a *view* of it.
const book = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../book' }),
});

export const collections = { book };
