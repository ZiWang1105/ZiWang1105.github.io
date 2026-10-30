# Deployment

The approved redesign targets https://ziwang1105.github.io/ and the `main` branch of `ZiWang1105/ZiWang1105.github.io`.

## GitHub Pages configuration

In repository **Settings → Pages**, choose **Deploy from a branch**, select **main** and **/ (root)**, then save. GitHub Pages was disabled before the redesign and must be enabled for the website to become accessible.

## Update the website

1. Edit the template, publication data, styles, or assets.
2. Run `python3 scripts/build.py` and `python3 scripts/verify.py`.
3. Commit the generated page with its source and assets to `main`.
4. Check the Pages deployment and verify https://ziwang1105.github.io/.

The site is static and requires no server-side runtime. `.nojekyll` bypasses Jekyll processing. Preserve the Google Search Console verification HTML file.

A separate owner-private design preview remains available at https://zi-wang-berkeley-research.snowycomet28.chatgpt.site. Its source checkout and hosting settings are independent of GitHub Pages.
