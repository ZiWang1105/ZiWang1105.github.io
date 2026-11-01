#!/usr/bin/env python3
"""Check generated content, local resources, and academic publication selection."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.references = []
        self.papers = []
        self.images = []
        self.videos = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ['href', 'src', 'poster', 'data-src']:
            if key in attrs:
                self.references.append(attrs[key])
        if tag == 'article' and 'paper' in attrs.get('class', '').split():
            self.papers.append(attrs)
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'video':
            self.videos.append(attrs)


def main():
    page = Page()
    source = (ROOT / 'index.html').read_text()
    page.feed(source)
    duplicates = [key for key, count in Counter(page.ids).items() if count > 1]
    assert not duplicates, f'Duplicate IDs: {duplicates}'
    for ref in page.references:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        if url.path:
            assert (ROOT / unquote(url.path)).is_file(), f'Missing asset: {ref}'
        elif url.fragment:
            assert url.fragment in page.ids, f'Broken anchor: {ref}'
    data = json.loads((ROOT / 'data/publications.json').read_text())
    expected = {'grail', 'sonic', 'doorman', 'viral', 'safehydra', 'chatsim', 'tbp-former'}
    actual = {p['id'] for p in data['papers'] if p['selected']}
    assert actual == expected, actual
    assert len(page.papers) == len(data['papers']) == 18
    assert len(page.videos) == 10
    for paper in data['papers']:
        assert (ROOT / f'assets/teasers/{paper["id"]}-poster.jpg').is_file(), f'Missing research image: {paper["id"]}'
    assert 'paper-typographic' not in source, 'Every paper must have an animation or a method figure.'
    assert all(image.get('alt') for image in page.images), 'An image is missing alternative text.'
    assert all('muted' in video and 'playsinline' in video for video in page.videos)
    assert 'Prof. Shankar Sastry' in source and 'BAIR' in source
    assert 'Previously, I was a Research Engineer' in source
    assert '{{' not in source
    print(f'PASS: {len(page.papers)} papers; {len(actual)} Selected; {len(page.videos)} video teasers; local links, IDs, and assets valid.')


if __name__ == '__main__':
    main()
