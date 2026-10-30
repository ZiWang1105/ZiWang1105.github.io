/* Optional interaction checks: npm install --no-save linkedom@0.18.12 */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { parseHTML } = require('linkedom');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const script = fs.readFileSync(path.join(root, 'scripts/site.js'), 'utf8');

function setup({ reduced = false, saveData = false, query = '' } = {}) {
  const { document, window } = parseHTML(source);
  let preferenceChange;
  const preferences = { matches: reduced, addEventListener: (_, callback) => { preferenceChange = callback; } };
  const pageWindow = {
    matchMedia: () => preferences,
    location: { search: query, href: `https://example.com/${query}` },
    history: { replaceState() {} }
  };
  for (const video of document.querySelectorAll('video')) {
    video.play = () => { video.playing = true; return Promise.resolve(); };
    video.pause = () => { video.playing = false; };
  }
  class Observer {
    constructor(callback) { this.callback = callback; }
    observe(target) { this.callback([{ target, isIntersecting: true }]); }
  }
  pageWindow.IntersectionObserver = Observer;
  vm.runInNewContext(script, {
    document, window: pageWindow, navigator: { connection: { saveData } },
    URL, URLSearchParams, IntersectionObserver: Observer
  });
  return {
    document,
    visible: () => [...document.querySelectorAll('.paper')].filter(p => !p.hidden),
    click: selector => document.querySelector(selector).click(),
    search: text => {
      const input = document.querySelector('#paper-search');
      input.value = text;
      input.dispatchEvent(new window.Event('input'));
    },
    preferenceChange: value => preferenceChange({ matches: value })
  };
}
const page = setup();
assert.equal(page.visible().length, 7);
assert.ok(page.visible().every(p => p.dataset.selected === 'true'));
const sonic = page.visible().find(p => p.id === 'paper-sonic');
assert.ok(sonic, 'SONIC should appear in the default Selected view');
assert.equal(sonic.querySelector('.paper-content > .authors').textContent, 'NVIDIA GEAR Team · Zi Wang (Core contributor)');
assert.equal(sonic.querySelector('.paper-content > .authors strong').textContent, 'Zi Wang');
const sonicAuthors = sonic.querySelector('.author-details .authors').textContent.split(', ');
assert.equal(sonicAuthors.length, 28);
assert.equal(sonicAuthors[0], 'Zhengyi Luo†');
assert.equal(sonicAuthors[4], 'Fernando Castañeda†');
assert.ok(sonicAuthors.includes('Zi Wang*'));
assert.equal(sonic.querySelector('.author-details .author-legend').textContent, '† (Co-)lead authors · * Core contributors · ‡ Equal advising.');
assert.equal(page.document.querySelector('#paper-grail .paper-content > .authors').textContent, 'Tianyi Xie*, Haotian Zhang*, Jinhyung Park*, Zi Wang*, …');
page.search('NVIDIA GEAR Team');
assert.deepEqual(page.visible().map(p => p.id), ['paper-sonic']);
page.click('[data-filter="all"]');
assert.deepEqual(page.visible().map(p => p.id), ['paper-sonic']);
page.click('[data-filter="selected"]');
assert.deepEqual(page.visible().map(p => p.id), ['paper-sonic']);
page.search('');
assert.equal(page.visible().length, 7);
page.click('[data-filter="all"]');
assert.equal(page.visible().length, 17);
page.search('Large Discrete Policy');
assert.equal(page.visible().length, 1);
assert.equal(page.visible()[0].id, 'paper-ldip');
page.click('[data-filter="selected"]');
assert.equal(page.visible().length, 0);
assert.equal(page.document.querySelector('#empty-results').hidden, false);
page.search('');
assert.equal(page.visible().length, 7);
page.search('CVPR 2024');
assert.equal(page.visible().length, 1);
assert.equal(page.visible()[0].id, 'paper-chatsim');
page.search('Zi Wang');
assert.equal(page.visible().length, 7);
page.click('#motion-toggle');
assert.ok([...page.document.querySelectorAll('video')].every(v => !v.playing));
page.click('#motion-toggle');
assert.ok([...page.document.querySelectorAll('.paper:not([hidden]) video')].every(v => v.playing));
page.preferenceChange(true);
assert.ok([...page.document.querySelectorAll('video')].every(v => !v.playing));
for (const options of [{ reduced: true }, { saveData: true }]) {
  const accessiblePage = setup(options);
  assert.ok([...accessiblePage.document.querySelectorAll('video')].every(v => !v.playing));
  assert.equal(accessiblePage.document.querySelector('#motion-toggle').textContent, 'Play teasers');
}
assert.equal(setup({ query: '?papers=all' }).visible().length, 17);
console.log('PASS: Selected/All, SONIC team credit and full authors, search by title/author/team/venue, empty results, deep link, pause/play, reduced motion, and data-saving behavior.');
