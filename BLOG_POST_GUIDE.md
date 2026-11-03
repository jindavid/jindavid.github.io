# How to send a blog post for jindavid.me

Send **one Markdown file** (plus any images) in the format below. It will be dropped into the site's `_posts/` folder as-is.

## 1. File name

```
YYYY-MM-DD-short-title.md
```

- Date = intended publish date, e.g. `2026-11-03-biloco.md`
- Lowercase, words separated by hyphens, no spaces. The part after the date becomes the URL.

## 2. Header (front matter)

The file must start with this block, exactly between the two `---` lines:

```yaml
---
layout: post
title: "BiLoCo: One-Bit Corrections for FP4 Decode"
subtitle: "Optional one-line summary shown under the title"
tags: [quantization, gpu]
---
```

| Field | Required | Notes |
|---|---|---|
| `layout` | yes | Always `post`. |
| `title` | yes | Wrap in double quotes (needed if it contains `:`). |
| `subtitle` | no | One sentence. Delete the line if unused. |
| `tags` | no | Short lowercase words, in `[ ]`, comma-separated. |

Do **not** add a `date:` field; the date comes from the file name.

## 3. Body

Plain Markdown (GitHub style):

- **First paragraph** should stand on its own as a 1–3 sentence summary.
- Section headings start at `##` (the title is already the top heading; don't use `#`).
- Code: fenced blocks with a language, e.g. ` ```python `.
- Links: `[text](https://...)`. Link papers to their arXiv page.
- Tables: standard Markdown pipe tables.
- Math: LaTeX with `$...$` inline and `$$...$$` on its own line for display equations (rendered by MathJax).
- No raw HTML, scripts, or embedded iframes unless agreed beforehand.

## 4. Images

- Send image files separately (PNG/JPG/SVG, under ~1 MB each, width ≤ 1600 px).
- Name them with the post slug as prefix: `biloco-fig1.png`, `biloco-fig2.png`.
- Reference them in the Markdown as:

```markdown
![Speedup of the fused kernel vs FP4-only GEMM](/assets/img/biloco-fig1.png)
```

The text in `[ ]` is alt text: describe what the figure shows.

## 5. Minimal example

```markdown
---
layout: post
title: "BiLoCo: One-Bit Corrections for FP4 Decode"
tags: [quantization, gpu]
---

FP4 quantization makes LLM decoding cheap on Blackwell GPUs but costs accuracy. BiLoCo recovers it with low-rank corrections stored as one-bit sign vectors.

## Why FP4 needs a correction

...

![Fused kernel overhead by rank](/assets/img/biloco-fig1.png)

## Results

...
```

## Checklist before sending

- [ ] File name is `YYYY-MM-DD-slug.md`
- [ ] Front matter has `layout: post` and a quoted `title`
- [ ] First paragraph is a short summary
- [ ] Headings use `##` and below
- [ ] Every image is attached and referenced as `/assets/img/<name>`
- [ ] No raw HTML or embeds (unless agreed)
