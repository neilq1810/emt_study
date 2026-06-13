// Remark plugin: render the manuscript's `figures/*.png` references as images.
//
// The book references each plot as an inline code span, e.g. `figures/ch55_x.png`,
// so the prose stays a single source of truth that also renders on plain GitHub.
// This plugin finds those spans and, after the paragraph that first mentions each
// figure, inserts a captioned <figure> whose <img src> is prefixed with the site
// base path (so it loads under /emt_study on GitHub Pages). Deduped per document.
const FIG_RE = /^figures\/[A-Za-z0-9_.\-]+\.png$/;

export default function remarkFigures({ base = '/' } = {}) {
  const b = base.endsWith('/') ? base : base + '/';
  return (tree) => {
    const seen = new Set();
    const visit = (node) => {
      if (!Array.isArray(node.children)) return;
      const out = [];
      for (const child of node.children) {
        visit(child);
        out.push(child);
        if (child.type === 'paragraph') {
          // collect inlineCode anywhere in the paragraph subtree (it may be nested
          // inside **bold** / *emphasis* spans), not just direct children.
          const codes = [];
          const collect = (n) => {
            if (n.type === 'inlineCode') codes.push(n);
            if (Array.isArray(n.children)) n.children.forEach(collect);
          };
          collect(child);
          for (const c of codes) {
            const v = c.value.trim();
            if (FIG_RE.test(v) && !seen.has(v)) {
              seen.add(v);
              const file = v.split('/').pop();
              out.push({
                type: 'html',
                value:
                  `<figure class="md-figure">` +
                  `<img src="${b}${v}" alt="${file}" loading="lazy" />` +
                  `<figcaption><code>${v}</code></figcaption>` +
                  `</figure>`,
              });
            }
          }
        }
      }
      node.children = out;
    };
    visit(tree);
    return tree;
  };
}
