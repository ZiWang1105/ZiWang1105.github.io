# Quick start

Open `index.html` directly, or run:

```bash
python3 -m http.server 8000
```

Visit `http://localhost:8000`. No dependencies are required to view the site.

Edit `templates/index.html` for your bio and background, and `data/publications.json` for papers. Then regenerate and check:

```bash
python3 scripts/build.py
python3 scripts/verify.py
```

Selected includes (co-)lead-authored papers and the explicitly selected SONIC collaboration. All includes the full curated publication list. The source notes document the Google Scholar access limitation and publication verification.

See `README.md` for source structure and accessibility details. See `DEPLOYMENT.md` before publishing. Publish from `main` and `/ (root)` in GitHub Pages settings.
