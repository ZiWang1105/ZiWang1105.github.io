# Zi Wang — Research Website

A static academic portfolio for Zi Wang, PhD student at UC Berkeley, affiliated with BAIR and the EMBER Center and advised by Prof. Shankar Sastry. NVIDIA is listed as a previous Research Engineer role.

## Preview

Open `index.html` directly in a browser. The site needs no framework, package installation, or build server. For an HTTP preview:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Update content

- `data/publications.json`: publication metadata, equal-contribution evidence, selection flags, and source URLs.
- `templates/index.html`: biography, education, profile links, and page structure.
- `css/site.css`: responsive layout and visual styling.
- `scripts/site.js`: Selected/All filtering, search, and teaser playback.
- `assets/teasers/`: research animations and still-image posters.
- `assets/fonts/`: self-hosted Inter and Newsreader fonts, with their OFL licenses and source records.
- `data/asset-sources.json`: original media sources and transformations.

After editing content or the template:

```bash
python3 scripts/build.py
python3 scripts/verify.py
```

The generated `index.html` contains every publication as ordinary HTML. JavaScript defaults to Selected and adds filtering. With JavaScript disabled, all papers remain readable. Use `?papers=all` to link directly to All.

## Selection rule

Selected contains six (co-)lead-authored papers and SONIC, an explicitly selected collaboration. The generator checks author and equal-contribution records along with the explicit collaboration flag. SONIC displays NVIDIA GEAR Team and identifies Zi Wang as a core contributor in its collapsed author summary. Its full 28-author list preserves the official contribution symbols and their paper-specific legend.

Current Selected list: GRAIL, SONIC, DoorMan, VIRAL, SafeHydra, ChatSim, and TBP-Former. All lists 18 works, including the Findings of EMNLP 2026 survey and clearly labelled technical reports.

## Motion and accessibility

Ten papers have looping, muted MP4 teasers. The other eight use method/framework or survey overview figures from the papers or their official publisher pages; click the figure or its Figure link to open it at full size. Every publication must have a real research visual: the build rejects missing media. Videos load near the viewport and pause when hidden, offscreen, or when the page is inactive. Reduced-motion preferences and data-saving mode disable autoplay. A visible Play/Pause teasers button controls motion. Posters remain available without JavaScript or autoplay.

## Publication verification

The existing repository links to Google Scholar profile `0SuL2yUAAAAJ`. Scholar blocked automated retrieval (HTTP 429) during this redesign. Publication details were cross-checked against official project pages, arXiv, conference/publisher records, and author homepages. This is not a complete Scholar export. The research notes in `data/publications.json` record unresolved identity and venue questions rather than silently adding uncertain claims.

## Deployment

The approved redesign is prepared for the `main` branch of `ZiWang1105/ZiWang1105.github.io`. The public website is https://ziwang1105.github.io/. See `DEPLOYMENT.md` for the GitHub Pages configuration and update steps. The separate Sites preview remains owner-private.

## Verification limits

Static checks validate local asset paths, HTML IDs, publication records, and the selected paper set. The JavaScript is syntax checked and the filters and motion controls are checked against a simulated DOM. A connected browser was unavailable for visual desktop/mobile QA; responsive styling is implemented but has not been verified in a real browser during this session.
