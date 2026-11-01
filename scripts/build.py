#!/usr/bin/env python3
"""Generate a dependency-free, GitHub Pages-compatible academic website."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/publications.json').read_text())
PAPERS = DATA['papers']


def escape(value):
    return html.escape(str(value), quote=True)


def author_markup(author):
    return f'<strong>{escape(author)}</strong>' if author.rstrip('*†‡') == 'Zi Wang' else escape(author)


def render_authors(authors, summary=None, contribution_role=None, legend=None):
    full = ', '.join(map(author_markup, authors))
    legend_markup = f'<p class="author-legend">{escape(legend)}</p>' if legend else ''
    if summary:
        role_markup = f' · <strong>Zi Wang</strong> ({escape(contribution_role)})' if contribution_role else ''
        return f'<p class="authors">{escape(summary)}{role_markup}</p><details class="author-details"><summary>All {len(authors)} authors</summary><p class="authors">{full}</p>{legend_markup}</details>'
    if len(authors) <= 14:
        return f'<p class="authors">{full}</p>'
    preview = authors[:4]
    zi = next(name for name in authors if name.rstrip('*†‡') == 'Zi Wang')
    if zi not in preview:
        preview.extend(['…', zi])
    preview.append('…')
    return f'<p class="authors">{", ".join(map(author_markup, preview))}</p><details class="author-details"><summary>All {len(authors)} authors</summary><p class="authors">{full}</p></details>'


def render_media(paper):
    slug = paper['id']
    path = f'assets/teasers/{slug}'
    poster = path + '-poster.jpg'
    video = path + '.mp4'
    project = paper['links'].get('project', paper['links']['paper'])
    label = {'doorman': 'DoorMan', 'safehydra': 'SafeHydra', 'chatsim': 'ChatSim',
             'tbp-former': 'TBP-Former', 'dialoguenerf': 'DialogueNeRF',
             'scorer-finetuning': 'Scorer fine-tuning', 'v2x-incop': 'V2X / InCoop',
             'drivesuprim': 'DriveSuprim', 'ldip': 'LDiP'}.get(slug, slug.upper())
    label = paper.get('media_label', label)
    if paper.get("media_kind") != "figure" and (ROOT / video).exists():
        return f'''<figure class="paper-media video-media" data-media="{escape(slug)}"><a href="{escape(project)}" aria-label="View {escape(label)} project or paper"><img src="{poster}" alt="{escape(label)} research demonstration" loading="lazy" width="800" height="500"><video data-src="{video}" poster="{poster}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video><span class="media-label">{escape(label)}</span></a></figure>'''
    if (ROOT / poster).exists():
        alt = paper.get('figure_alt', f'{label} method and framework diagram')
        return f'<figure class="paper-media figure-media" data-media="{escape(slug)}"><a href="{poster}" aria-label="Open full-size figure for {escape(label)}"><img src="{poster}" alt="{escape(alt)}" loading="lazy" width="800" height="500"></a></figure>'
    raise FileNotFoundError(f'{slug}: add a research animation or a method-figure poster before building.')


def render_paper(paper):
    title = escape(paper['title'])
    destination = escape(paper['links'].get('project', paper['links']['paper']))
    venue = paper['venue']
    if str(paper['year']) not in venue:
        venue += f' · {paper["year"]}'
    badge = f'<span class="badge">{escape(paper["distinction"])}</span>' if paper.get('distinction') else ''
    links = []
    for kind, label in [('project', 'Project'), ('paper', 'Paper'), ('code', 'Code'), ('doi', 'Journal')]:
        if kind in paper['links']:
            links.append(f'<a href="{escape(paper["links"][kind])}" aria-label="{label}: {title}">{label} <span aria-hidden="true">↗</span></a>')
    if paper.get('media_kind') == 'figure' or not (ROOT / f'assets/teasers/{paper["id"]}.mp4').exists():
        links.append(f'<a href="assets/teasers/{paper["id"]}-poster.jpg" aria-label="Full-size figure: {title}">Figure <span aria-hidden="true">↗</span></a>')
    query = escape(' '.join(filter(None, [paper['title'], ' '.join(paper['authors']), paper.get('author_summary', ''), venue, paper['id']])).lower())
    return f'''        <article class="paper" id="paper-{paper['id']}" data-selected="{str(paper['selected']).lower()}" data-search="{query}" aria-labelledby="title-{paper['id']}">
          {render_media(paper)}
          <div class="paper-content">
            <p class="paper-meta"><span class="venue">{escape(venue)}</span>{badge}</p>
            <h3 id="title-{paper['id']}"><a href="{destination}">{title}</a></h3>
            {render_authors(paper['authors'], paper.get('author_summary'), paper.get('contribution_role'), paper.get('author_legend'))}
            <p class="paper-summary">{escape(paper['summary'])}</p>
            <div class="paper-links">{' '.join(links)}</div>
          </div>
        </article>'''


def main():
    assert len({paper['id'] for paper in PAPERS}) == len(PAPERS), 'Paper IDs must be unique.'
    for paper in PAPERS:
        assert any(name.rstrip('*†‡') == 'Zi Wang' for name in paper['authors']), paper['id']
        is_lead = paper['authors'][0].rstrip('*†‡') == 'Zi Wang' or 'Zi Wang' in paper.get('equal_first_authors', [])
        expected = is_lead or paper.get('selected_collaboration', False)
        assert paper['selected'] == expected, f'Selection mismatch: {paper["id"]}'
    page = (ROOT / 'templates/index.html').read_text()
    replacements = {
        '{{PAPERS}}': '\n'.join(map(render_paper, PAPERS)),
        '{{SELECTED_COUNT}}': str(sum(p['selected'] for p in PAPERS)),
        '{{ALL_COUNT}}': str(len(PAPERS)),
        '{{YEAR}}': '2026',
    }
    for token, value in replacements.items():
        page = page.replace(token, value)
    assert '{{' not in page, 'Unfilled template token.'
    (ROOT / 'index.html').write_text(page)
    print(f'Built index.html: {len(PAPERS)} papers, {sum(p["selected"] for p in PAPERS)} selected.')


if __name__ == '__main__':
    main()
