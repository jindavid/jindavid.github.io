# David Jin's personal website

A minimal Jekyll website with a narrow reading column, white background, dark monospaced text, and blue links. The simple layout is inspired by https://ssi.inc/ and uses the requested brighter palette.

## Editing

- Edit `index.md` for the homepage introduction.
- Edit `_data/profile.yml` for your name, affiliation, and profile links.
- Edit `cv.md` for the full CV, based on the supplied LaTeX.
- Add publications to `_bibliography/publications.bib`. Set `selected = {true}` and `research_area = {optimization}` or `research_area = {machine_learning}` to show a paper in the corresponding homepage research area. Use `status = {submitted}` for manuscripts and `status = {published}` for conference and journal papers. `presentation_label` controls the displayed venue, and `author_marks` preserves the CV's asterisk markers by author position.
- Add dated Markdown files to `_posts/` with `layout: post` to publish writing.
- Edit `assets/css/personal.css` for the design.

The original theme's demonstration posts, presentation, and hub remain in the source but are excluded from the generated website. The blog is ready for your own posts.

## Local preview

```sh
bundle install
bundle exec jekyll serve
```

Open http://127.0.0.1:4000/ while the server is running. The CV-based revision is a local demo; it has not been published.

## Build

```sh
bundle exec jekyll build
```

## CV PDF

The CV page links to `assets/pdf/David-Jin-CV.pdf`. The PDF is generated from the current CV page, including the bibliography, so removed website content stays out of the download. After editing the CV or publications, refresh the PDF with Python and ReportLab installed:

```sh
bundle exec jekyll build
python3 _scripts/build_cv_pdf.py _site/cv.html assets/pdf/David-Jin-CV.pdf
bundle exec jekyll build
```

The GitHub Pages workflow publishes the `_site/` output. Sites uses the same Jekyll source, built with `--destination dist`, and the private project specified in `.openai/hosting.json`.

This project originally used Grape Academic Theme. Its original MIT license is retained in `LICENSE.txt`.
