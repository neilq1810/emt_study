// Copy the repo-root /figures and /data (produced by simulations/run_all.py)
// into dashboard/public so Astro serves them at ${base}/figures and ${base}/data.
// Runs automatically before `build`/`dev` via the npm pre-hooks. The copies are
// gitignored; the originals in /figures and /data are the source of truth.
import { cp, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(process.cwd(), '..');
const pub = resolve(process.cwd(), 'public');

for (const dir of ['figures', 'data']) {
  const src = resolve(root, dir);
  const dst = resolve(pub, dir);
  if (existsSync(src)) {
    await mkdir(pub, { recursive: true });
    await cp(src, dst, { recursive: true });
    console.log(`[copy-assets] ${dir}/ -> public/${dir}/`);
  } else {
    console.warn(`[copy-assets] skipped: ${src} not found`);
  }
}
