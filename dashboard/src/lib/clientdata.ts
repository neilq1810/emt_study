// Client-side fetch helpers for the Phase-5 simulation outputs served from
// /data (copied there from the repo-root /data by scripts/copy-assets.mjs).
// Lets the interactive tools display the canonical NumPy/SciPy `emtrack` numbers
// alongside their live TypeScript results, demonstrating the two agree.

export const DATA_BASE = import.meta.env.BASE_URL.replace(/\/$/, '') + '/data';

export async function fetchJson<T = any>(name: string): Promise<T | null> {
  try {
    const r = await fetch(`${DATA_BASE}/${name}`);
    return r.ok ? ((await r.json()) as T) : null;
  } catch {
    return null;
  }
}

export async function fetchCsv(name: string): Promise<Record<string, number>[]> {
  try {
    const r = await fetch(`${DATA_BASE}/${name}`);
    if (!r.ok) return [];
    const text = (await r.text()).trim();
    const [head, ...rows] = text.split(/\r?\n/);
    const cols = head.split(',');
    return rows.map((line) => {
      const vals = line.split(',');
      return Object.fromEntries(cols.map((c, i) => [c, Number(vals[i])]));
    });
  } catch {
    return [];
  }
}
