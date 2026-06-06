// Build-time loader for the repository bibliography (the single source of truth
// for references). Read in .astro frontmatter only (Node fs); never client-side.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

export interface BibEntry {
  id: string;
  type?: string;
  title: string;
  authors?: string[];
  year?: number;
  venue?: string;
  doi?: string;
  url?: string;
  source_type?: string;
  keywords?: string[];
  relevance?: number;
  confidence?: string;
  notes?: string;
}

export function loadBib(): { entries: BibEntry[]; byId: Record<string, BibEntry> } {
  // cwd is the Astro project root (dashboard/) during build.
  const path = resolve(process.cwd(), '..', 'citations', 'bibliography.json');
  const data = JSON.parse(readFileSync(path, 'utf8'));
  const entries: BibEntry[] = data.entries ?? [];
  const byId: Record<string, BibEntry> = {};
  for (const e of entries) byId[e.id] = e;
  return { entries, byId };
}

export function authorsShort(e: BibEntry): string {
  const a = e.authors ?? [];
  if (a.length === 0) return '';
  const first = a[0].split(',')[0];
  return a.length === 1 ? first : `${first} et al.`;
}
