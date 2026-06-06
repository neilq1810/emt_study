// Build a structured table of contents from the `book` content collection.
// Chapter files have no frontmatter; we derive titles from the first H1 and
// part grouping from the directory name (e.g. "part-02-electromagnetic-theory").

export interface BookEntryLike {
  id: string;
  body?: string;
}

export interface ChapterItem {
  id: string;
  title: string;
}

export interface PartGroup {
  key: string; // directory key or "_root"
  label: string; // e.g. "Part II · Electromagnetic Theory"
  order: number;
  items: ChapterItem[];
}

const ROMAN = [
  '', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
  'XIII', 'XIV', 'XV', 'XVI',
];

function titleCase(s: string): string {
  return s
    .split('-')
    .map((w) => (w.length ? w[0].toUpperCase() + w.slice(1) : w))
    .join(' ');
}

/** Extract a human title from the first Markdown H1, falling back to the id. */
export function extractTitle(entry: BookEntryLike): string {
  const body = entry.body ?? '';
  const m = body.match(/^#\s+(.+?)\s*$/m);
  if (m) return m[1].replace(/\s*\{#.*\}\s*$/, '').trim();
  return entry.id;
}

/** Parse the part directory key ("part-02-electromagnetic-theory") into a label. */
function partLabel(key: string): { label: string; order: number } {
  const m = key.match(/^part-(\d+)-(.+)$/);
  if (!m) return { label: titleCase(key), order: 999 };
  const num = parseInt(m[1], 10);
  const roman = ROMAN[num] ?? String(num);
  return { label: `Part ${roman} · ${titleCase(m[2])}`, order: num };
}

export function chapterMeta(entry: BookEntryLike): { title: string; partKey: string } {
  const slashIdx = entry.id.indexOf('/');
  const partKey = slashIdx >= 0 ? entry.id.slice(0, slashIdx) : '_root';
  return { title: extractTitle(entry), partKey };
}

export function buildToc(entries: BookEntryLike[]): PartGroup[] {
  const groups = new Map<string, PartGroup>();

  for (const entry of entries) {
    const { title, partKey } = chapterMeta(entry);
    if (!groups.has(partKey)) {
      if (partKey === '_root') {
        groups.set(partKey, { key: partKey, label: 'Reference', order: 1000, items: [] });
      } else {
        const { label, order } = partLabel(partKey);
        groups.set(partKey, { key: partKey, label, order, items: [] });
      }
    }
    groups.get(partKey)!.items.push({ id: entry.id, title });
  }

  const result = [...groups.values()];
  result.sort((a, b) => a.order - b.order);
  for (const g of result) g.items.sort((a, b) => a.id.localeCompare(b.id));
  return result;
}

/** Base-aware link to a chapter route. */
export function chapterHref(base: string, id: string): string {
  const b = base.endsWith('/') ? base : base + '/';
  return `${b}book/${id}`;
}
