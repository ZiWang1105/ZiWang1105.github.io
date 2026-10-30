/* Progressive enhancement: complete publication content remains readable without JS. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const papers = [...document.querySelectorAll('.paper')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const search = document.querySelector('#paper-search');
  const description = document.querySelector('#publication-description');
  const status = document.querySelector('#result-status');
  const empty = document.querySelector('#empty-results');
  const motionButton = document.querySelector('#motion-toggle');
  const videos = [...document.querySelectorAll('.paper video')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  let animationEnabled = !reducedMotion.matches && !connection?.saveData;
  let filter = new URLSearchParams(window.location.search).get('papers') === 'all' ? 'all' : 'selected';
  const inView = new Set();

  function updateVideo(video) {
    const visible = !video.closest('.paper').hidden && inView.has(video);
    if (animationEnabled && visible && !document.hidden) {
      if (!video.src && video.dataset.src) video.src = video.dataset.src;
      video.play().catch(() => { /* A poster remains visible when autoplay is unavailable. */ });
    } else {
      video.pause();
    }
  }
  function updateMotionButton() {
    motionButton.textContent = animationEnabled ? 'Pause teasers' : 'Play teasers';
    motionButton.setAttribute('aria-pressed', String(animationEnabled));
  }
  function applyFilter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    papers.forEach(paper => {
      const matches = (filter === 'all' || paper.dataset.selected === 'true') &&
        (!query || paper.dataset.search.includes(query));
      paper.hidden = !matches;
      if (matches) count += 1;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === filter)));
    description.textContent = filter === 'selected' ?
      '(Co-)lead-authored papers and selected collaborations. * Equal contribution unless noted.' :
      'All publications, newest first. * Equal contribution unless noted.';
    status.textContent = `${count} ${count === 1 ? 'publication' : 'publications'}${query ? ' matching your search' : ''}`;
    empty.hidden = count !== 0;
    videos.forEach(updateVideo);
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    filter = button.dataset.filter;
    applyFilter();
    const url = new URL(window.location.href);
    if (filter === 'all') url.searchParams.set('papers', 'all');
    else url.searchParams.delete('papers');
    try { window.history.replaceState({}, '', url); } catch (_) { /* Local file previews may restrict history. */ }
  }));
  search.addEventListener('input', applyFilter);
  motionButton.addEventListener('click', () => {
    animationEnabled = !animationEnabled;
    updateMotionButton();
    videos.forEach(updateVideo);
  });
  reducedMotion.addEventListener('change', event => {
    animationEnabled = !event.matches && !connection?.saveData;
    updateMotionButton();
    videos.forEach(updateVideo);
  });
  document.addEventListener('visibilitychange', () => videos.forEach(updateVideo));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) inView.add(entry.target);
        else inView.delete(entry.target);
        updateVideo(entry.target);
      });
    }, {rootMargin: '100px 0px', threshold: 0.05});
    videos.forEach(video => observer.observe(video));
  } else {
    videos.forEach(video => inView.add(video));
  }
  updateMotionButton();
  applyFilter();
})();
