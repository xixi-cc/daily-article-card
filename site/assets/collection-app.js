/**
 * Unified Daily / Collection reader. The parent build serves this source as
 * assets/app.js and collection-app.js; it consumes only assets/all-data.json.
 * Calendar pages stay anchored to actual collection dates, even while filtering.
 */
if (!window.PaperImageViewer) {
/**
 * @file media.js
 * @description 通用论文图片灯箱：支持点击放大、滚轮缩放、拖拽查看和键盘关闭。
 */
(function(){
  let lightboxEl = null;
  let imageEl = null;
  let captionEl = null;
  let scaleLabelEl = null;
  let closeButtonEl = null;
  let imageScale = 1;
  let imageOffsetX = 0;
  let imageOffsetY = 0;
  let dragStartX = 0;
  let dragStartY = 0;
  let dragOriginX = 0;
  let dragOriginY = 0;
  let activePointerId = null;
  let returnFocusEl = null;

  function clampScale(value){
    return Math.min(4, Math.max(1, value));
  }

  function renderTransform(){
    if(!imageEl || !scaleLabelEl){
      return;
    }

    imageEl.style.transform = `translate3d(${imageOffsetX}px, ${imageOffsetY}px, 0) scale(${imageScale})`;
    imageEl.classList.toggle('is-zoomed', imageScale > 1);
    scaleLabelEl.textContent = `${Math.round(imageScale * 100)}%`;
  }

  function setScale(nextScale){
    const normalizedScale = clampScale(nextScale);
    if(normalizedScale === 1){
      imageOffsetX = 0;
      imageOffsetY = 0;
    }
    imageScale = normalizedScale;
    renderTransform();
  }

  function resetImagePosition(){
    imageScale = 1;
    imageOffsetX = 0;
    imageOffsetY = 0;
    renderTransform();
  }

  function ensureLightbox(){
    if(lightboxEl){
      return;
    }

    lightboxEl = document.createElement('div');
    lightboxEl.className = 'image-lightbox';
    lightboxEl.setAttribute('aria-hidden', 'true');
    lightboxEl.innerHTML = `
      <div class="image-lightbox-stage" data-image-lightbox-close>
        <img class="image-lightbox-image" alt="" draggable="false" />
      </div>
      <div class="image-lightbox-topbar">
        <p class="image-lightbox-caption"></p>
        <button class="image-lightbox-close" type="button" aria-label="关闭图片预览">×</button>
      </div>
      <div class="image-lightbox-controls" aria-label="图片缩放控制">
        <button type="button" data-image-zoom-out aria-label="缩小图片">−</button>
        <button class="image-lightbox-scale" type="button" data-image-zoom-reset aria-label="恢复原始缩放">100%</button>
        <button type="button" data-image-zoom-in aria-label="放大图片">+</button>
      </div>
    `;

    document.body.appendChild(lightboxEl);
    imageEl = lightboxEl.querySelector('.image-lightbox-image');
    captionEl = lightboxEl.querySelector('.image-lightbox-caption');
    scaleLabelEl = lightboxEl.querySelector('.image-lightbox-scale');
    closeButtonEl = lightboxEl.querySelector('.image-lightbox-close');
    const stageEl = lightboxEl.querySelector('.image-lightbox-stage');

    lightboxEl.addEventListener('click', (event) => {
      if(event.target.closest('[data-image-lightbox-close]') && event.target !== imageEl){
        close();
      }
    });

    closeButtonEl.addEventListener('click', close);
    lightboxEl.querySelector('[data-image-zoom-out]').addEventListener('click', () => setScale(imageScale - 0.5));
    lightboxEl.querySelector('[data-image-zoom-in]').addEventListener('click', () => setScale(imageScale + 0.5));
    lightboxEl.querySelector('[data-image-zoom-reset]').addEventListener('click', resetImagePosition);

    stageEl.addEventListener('wheel', (event) => {
      if(!lightboxEl.classList.contains('is-open')){
        return;
      }
      event.preventDefault();
      setScale(imageScale + (event.deltaY < 0 ? 0.25 : -0.25));
    }, { passive: false });

    imageEl.addEventListener('dblclick', () => {
      setScale(imageScale > 1 ? 1 : 2);
    });

    imageEl.addEventListener('pointerdown', (event) => {
      if(imageScale <= 1){
        return;
      }
      activePointerId = event.pointerId;
      dragStartX = event.clientX;
      dragStartY = event.clientY;
      dragOriginX = imageOffsetX;
      dragOriginY = imageOffsetY;
      imageEl.setPointerCapture(event.pointerId);
      imageEl.classList.add('is-dragging');
    });

    imageEl.addEventListener('pointermove', (event) => {
      if(activePointerId !== event.pointerId){
        return;
      }
      imageOffsetX = dragOriginX + event.clientX - dragStartX;
      imageOffsetY = dragOriginY + event.clientY - dragStartY;
      renderTransform();
    });

    function stopDragging(event){
      if(activePointerId !== event.pointerId){
        return;
      }
      activePointerId = null;
      imageEl.classList.remove('is-dragging');
    }

    imageEl.addEventListener('pointerup', stopDragging);
    imageEl.addEventListener('pointercancel', stopDragging);

    window.addEventListener('keydown', (event) => {
      if(!lightboxEl.classList.contains('is-open')){
        return;
      }
      if(event.key === 'Escape'){
        event.preventDefault();
        close();
      }
      if(event.key === '+' || event.key === '='){
        setScale(imageScale + 0.5);
      }
      if(event.key === '-'){
        setScale(imageScale - 0.5);
      }
    });
  }

  function open(options){
    if(!options || !options.src){
      return;
    }

    ensureLightbox();
    returnFocusEl = options.returnFocus || document.activeElement;
    imageEl.src = options.src;
    imageEl.alt = options.alt || '论文图片放大预览';
    captionEl.textContent = options.caption || options.alt || '';
    captionEl.classList.toggle('hidden', !captionEl.textContent);
    resetImagePosition();
    lightboxEl.classList.add('is-open');
    lightboxEl.setAttribute('aria-hidden', 'false');
    document.body.classList.add('has-image-lightbox');
    window.requestAnimationFrame(() => closeButtonEl.focus());
  }

  function close(){
    if(!lightboxEl || !lightboxEl.classList.contains('is-open')){
      return;
    }

    lightboxEl.classList.remove('is-open');
    lightboxEl.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('has-image-lightbox');
    imageEl.removeAttribute('src');
    if(returnFocusEl && typeof returnFocusEl.focus === 'function'){
      returnFocusEl.focus({ preventScroll: true });
    }
    returnFocusEl = null;
  }

  function isOpen(){
    return Boolean(lightboxEl && lightboxEl.classList.contains('is-open'));
  }

  window.PaperImageViewer = { open, close, isOpen };
})();
}
(function(){
  'use strict';
  let DATA = [];
  const $ = (selector) => document.querySelector(selector);
  const statusEl = $('#status');
  const groupsEl = $('#groups');
  const searchEl = $('#search');
  const tagFilterEl = $('#tag-filter');
  const modeEl = $('#browse-mode');
  const gradeEl = $('#grade-filter');
  const paperCountEl = $('#paper-count');
  const paginationEl = $('#pagination');
  const favoritesStorageKey = 'xixi-paper-favorites-v1';
  const paperModalQueryKey = 'paper';
  const favoriteItems = new WeakMap();
  let FAVORITES = readFavorites();
  let state = {mode: 'daily', page: 1, tag: '', grade: 'all', q: ''};
  let loaded = false;
  let paperModalEl = null;
  let paperModalFrameEl = null;
  let paperModalTitleEl = null;
  let paperModalOpenLinkEl = null;
  let paperModalLoaderEl = null;
  let modalReturnFocusEl = null;
  let modalCleanupTimerId = null;
  let modalSessionId = 0;
  let openIdentifier = null;

  function readFavorites(){
    try{
      const parsed = JSON.parse(window.localStorage.getItem(favoritesStorageKey) || '[]');
      return Array.isArray(parsed) ? Array.from(new Set(parsed.filter((value) => typeof value === 'string'))).sort() : [];
    } catch (error) {
      console.warn('读取收藏失败', error);
      return [];
    }
  }

  function writeFavorites(values){
    FAVORITES = Array.from(new Set(values)).sort();
    try{
      window.localStorage.setItem(favoritesStorageKey, JSON.stringify(FAVORITES));
    } catch (error) {
      console.warn('保存收藏失败', error);
    }
  }

  function getFavoriteKeys(item){
    const program = String(item.detail_path || '').startsWith('collection-papers/') ? 'collection' : 'daily';
    const primary = `${program}:${item.arxiv_id || item.detail_path}`;
    const aliases = Array.isArray(item.favorite_keys) ? item.favorite_keys : [];
    return Array.from(new Set([primary, ...aliases].filter(key => typeof key === 'string' && key)));
  }

  function isFavorite(item){
    return getFavoriteKeys(item).some(key => FAVORITES.includes(key));
  }

  function updateFavoriteButtons(){
    document.querySelectorAll('.feed-favorite-button').forEach(button => {
      const item = favoriteItems.get(button);
      if(!item) return;
      const favorite = isFavorite(item);
      button.textContent = favorite ? '★' : '☆';
      button.setAttribute('aria-pressed', String(favorite));
      button.setAttribute('aria-label', `${favorite ? '取消收藏' : '收藏'}：${item.title || '论文'}`);
      button.title = favorite ? '取消收藏' : '收藏';
    });
  }

  function toggleFavorite(item){
    const keys = getFavoriteKeys(item);
    writeFavorites(isFavorite(item) ? FAVORITES.filter(key => !keys.includes(key)) : [...FAVORITES, ...keys]);
    updateFavoriteButtons();
  }

  // A detail page edits its own legacy key. Mirror that change to all aliases
  // so removing a favorite there also removes the deduplicated list's star.
  function refreshFavorites(changedKey){
    const previous = FAVORITES;
    const next = readFavorites();
    const changed = changedKey ? [changedKey] : [...new Set([...previous, ...next])]
      .filter(key => previous.includes(key) !== next.includes(key));
    let values = next.slice();
    DATA.forEach(item => {
      const keys = getFavoriteKeys(item);
      const key = changed.find(value => keys.includes(value));
      if(!key) return;
      values = next.includes(key) ? [...values, ...keys] : values.filter(value => !keys.includes(value));
    });
    const normalized = Array.from(new Set(values)).sort();
    if(JSON.stringify(normalized) !== JSON.stringify(next)) writeFavorites(normalized);
    else FAVORITES = next;
    updateFavoriteButtons();
  }

  function saveCatalogReturnURL(){
    try {
      const url = new URL(window.location.href);
      url.searchParams.delete(paperModalQueryKey);
      window.sessionStorage.setItem('paper-catalog-return-url', url.href);
    } catch(error){ console.warn('保存目录返回地址失败', error); }
  }

  function getPaperIdentifier(item){
    return String(item.arxiv_id || item.detail_path || '');
  }

  function getStandalonePaperURL(detailPath){
    return new URL(detailPath, window.location.href).href;
  }

  function getEmbeddedPaperURL(detailPath){
    const embeddedURL = new URL(detailPath, window.location.href);
    embeddedURL.searchParams.set('embed', '1');
    return embeddedURL.href;
  }

  function replacePaperModalFrameLocation(frameURL){
    if(!paperModalFrameEl){
      return;
    }

    try {
      if(paperModalFrameEl.contentWindow){
        paperModalFrameEl.contentWindow.location.replace(frameURL);
        return;
      }
    } catch (error) {
      console.warn('无法替换论文浮窗地址，改用 iframe src 导航', error);
    }

    paperModalFrameEl.src = frameURL;
  }

  function ensurePaperModal(){
    if(paperModalEl){
      return;
    }

    paperModalEl = document.createElement('div');
    paperModalEl.className = 'paper-modal';
    paperModalEl.setAttribute('aria-hidden', 'true');
    paperModalEl.innerHTML = `
      <div class="paper-modal-backdrop" data-paper-modal-close></div>
      <section class="paper-modal-panel" role="dialog" aria-modal="true" aria-labelledby="paper-modal-title">
        <header class="paper-modal-toolbar">
          <div class="paper-modal-heading">
            <span class="paper-modal-kicker">论文阅读</span>
            <span id="paper-modal-title" class="paper-modal-title"></span>
          </div>
          <div class="paper-modal-actions">
            <a class="paper-modal-open-link" href="#" target="_blank" rel="noopener noreferrer">新页面打开 ↗</a>
            <button class="paper-modal-close" type="button" aria-label="关闭论文浮窗">×</button>
          </div>
        </header>
        <div class="paper-modal-content">
          <div class="paper-modal-loader" aria-hidden="true">
            <span class="paper-modal-spinner"></span>
            <span>正在打开论文阅读卡</span>
          </div>
          <iframe class="paper-modal-frame" title="论文详情" loading="eager"></iframe>
        </div>
      </section>
    `;

    document.body.appendChild(paperModalEl);
    paperModalFrameEl = paperModalEl.querySelector('.paper-modal-frame');
    paperModalTitleEl = paperModalEl.querySelector('.paper-modal-title');
    paperModalOpenLinkEl = paperModalEl.querySelector('.paper-modal-open-link');
    paperModalLoaderEl = paperModalEl.querySelector('.paper-modal-loader');

    paperModalEl.querySelector('[data-paper-modal-close]').addEventListener('click', requestClosePaperModal);
    paperModalEl.querySelector('.paper-modal-close').addEventListener('click', requestClosePaperModal);
    paperModalFrameEl.addEventListener('load', () => {
      connectPaperModalImageZoom();
      paperModalLoaderEl.classList.add('hidden');
      paperModalFrameEl.classList.add('is-ready');
    });
  }

  function connectPaperModalImageZoom(){
    if(!paperModalFrameEl || !window.PaperImageViewer){
      return;
    }

    let frameDocument = null;
    try {
      frameDocument = paperModalFrameEl.contentDocument;
    } catch (error) {
      console.warn('无法访问论文浮窗内容，保留嵌入页自身的图片预览逻辑', error);
      return;
    }

    if(!frameDocument){
      return;
    }

    frameDocument.querySelectorAll('.paper-figure-image').forEach((imageEl) => {
      if(imageEl.dataset.parentZoomBound === 'true'){
        return;
      }
      imageEl.dataset.parentZoomBound = 'true';

      const openImage = (event) => {
        event.preventDefault();
        event.stopPropagation();
        const figureEl = imageEl.closest('.paper-figure-card');
        const captionEl = figureEl ? figureEl.querySelector('.paper-figure-caption') : null;
        window.PaperImageViewer.open({
          src: imageEl.currentSrc || imageEl.src,
          alt: imageEl.alt || '论文图片',
          caption: captionEl ? captionEl.textContent.trim() : imageEl.alt || ''
        });
      };

      imageEl.addEventListener('click', openImage, true);
      imageEl.addEventListener('keydown', (event) => {
        if(event.key === 'Enter' || event.key === ' '){
          openImage(event);
        }
      }, true);
    });
  }

  function openPaperModal(item, options){
    if(!item || !item.detail_path){
      return;
    }

    saveCatalogReturnURL();
    const settings = options || {};
    ensurePaperModal();
    openIdentifier = getPaperIdentifier(item);
    modalSessionId += 1;
    if(modalCleanupTimerId !== null){
      window.clearTimeout(modalCleanupTimerId);
      modalCleanupTimerId = null;
    }
    modalReturnFocusEl = settings.returnFocus || modalReturnFocusEl || document.activeElement;
    if(window.MathJax?.typesetClear){ MathJax.typesetClear([paperModalTitleEl]); }
    paperModalTitleEl.textContent = item.title || '论文详情';
    typesetSurface(paperModalTitleEl);
    paperModalOpenLinkEl.href = getStandalonePaperURL(item.detail_path);
    paperModalFrameEl.title = `论文详情：${item.title || ''}`;
    paperModalFrameEl.classList.remove('is-ready');
    paperModalLoaderEl.classList.remove('hidden');
    replacePaperModalFrameLocation(getEmbeddedPaperURL(item.detail_path));
    paperModalEl.classList.add('is-open');
    paperModalEl.setAttribute('aria-hidden', 'false');
    document.body.classList.add('has-paper-modal');

    if(settings.updateHistory){
      const modalURL = new URL(window.location.href);
      const paperIdentifier = getPaperIdentifier(item);
      const currentHistoryState = window.history.state && typeof window.history.state === 'object'
        ? window.history.state
        : {};
      modalURL.searchParams.set(paperModalQueryKey, paperIdentifier);
      window.history.pushState(
        { ...currentHistoryState, paperModal: paperIdentifier },
        '',
        modalURL
      );
    }

    window.requestAnimationFrame(() => {
      paperModalEl.querySelector('.paper-modal-close').focus();
    });
  }

  function hidePaperModal(){
    if(!paperModalEl || !paperModalEl.classList.contains('is-open')){
      return;
    }

    openIdentifier = null;
    if(window.PaperImageViewer?.isOpen()) window.PaperImageViewer.close();
    const closingSessionId = modalSessionId;
    paperModalEl.classList.remove('is-open');
    paperModalEl.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('has-paper-modal');
    if(modalCleanupTimerId !== null){
      window.clearTimeout(modalCleanupTimerId);
    }
    modalCleanupTimerId = window.setTimeout(() => {
      modalCleanupTimerId = null;
      const modalWasNotReopened = modalSessionId === closingSessionId;
      if(modalWasNotReopened && !paperModalEl.classList.contains('is-open')){
        replacePaperModalFrameLocation('about:blank');
      }
    }, 220);

    if(modalReturnFocusEl && typeof modalReturnFocusEl.focus === 'function'){
      modalReturnFocusEl.focus({ preventScroll: true });
    }
    modalReturnFocusEl = null;
  }

  function requestClosePaperModal(){
    if(window.PaperImageViewer && window.PaperImageViewer.isOpen()){
      window.PaperImageViewer.close();
      return;
    }

    const modalURL = new URL(window.location.href);
    const paperIdentifier = modalURL.searchParams.get(paperModalQueryKey);
    const historyPaperIdentifier = window.history.state && typeof window.history.state === 'object'
      ? window.history.state.paperModal
      : null;
    const canReturnToPreviousHistoryEntry = Boolean(
      paperIdentifier && historyPaperIdentifier === paperIdentifier
    );

    hidePaperModal();

    if(canReturnToPreviousHistoryEntry){
      window.history.back();
      return;
    }

    modalURL.searchParams.delete(paperModalQueryKey);
    const replacementHistoryState = window.history.state && typeof window.history.state === 'object'
      ? { ...window.history.state }
      : null;
    if(replacementHistoryState){
      delete replacementHistoryState.paperModal;
    }
    window.history.replaceState(replacementHistoryState, '', modalURL);
  }

  function openPaperModalFromURL(){
    const paperIdentifier = new URL(window.location.href).searchParams.get(paperModalQueryKey);
    if(!paperIdentifier){
      hidePaperModal();
      return;
    }

    const item = DATA.find(candidate => getPaperIdentifier(candidate) === paperIdentifier || candidate.detail_path === paperIdentifier);
    if(item && openIdentifier !== getPaperIdentifier(item)){
      openPaperModal(item, { updateHistory: false });
    } else if(!item){
      hidePaperModal();
    }
  }

  function openPaperImage(item, imageEl){
    if(!window.PaperImageViewer){
      return;
    }

    window.PaperImageViewer.open({
      src: item.paper_image_full_path || item.paper_image_path || item.fallback_image_path || imageEl.currentSrc || imageEl.src,
      alt: item.title || imageEl.alt,
      caption: item.title || '',
      returnFocus: imageEl
    });
  }

  function applyCoverTheme(el, theme){
    if(!el || !theme){
      return;
    }

    const vars = {
      from: '--cover-from',
      to: '--cover-to',
      spot: '--cover-spot',
      ink: '--cover-ink',
      muted: '--cover-muted',
      chip: '--cover-chip',
      stroke: '--cover-stroke'
    };

    Object.entries(vars).forEach(([key, cssVar]) => {
      if(theme[key]){
        el.style.setProperty(cssVar, theme[key]);
      }
    });
  }

  function clearStatus(){
    statusEl.innerHTML = '';
    statusEl.classList.add('hidden');
  }

  function renderStatus(state, title, text, action){
    statusEl.classList.remove('hidden');
    statusEl.innerHTML = '';

    const card = document.createElement('div');
    card.className = 'status-card';
    card.dataset.state = state;

    const titleEl = document.createElement('div');
    titleEl.className = 'status-title';
    titleEl.textContent = title;

    const textEl = document.createElement('div');
    textEl.className = 'status-text';
    textEl.textContent = text;

    card.appendChild(titleEl);
    card.appendChild(textEl);

    if(action){
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'status-action';
      button.textContent = action.label;
      button.addEventListener('click', action.onClick);
      card.appendChild(button);
    }

    statusEl.appendChild(card);
  }

  // Reader-facing subjects consolidate aliases. Original tags remain searchable
  // and usable by old shared links; production classifications are unchanged.
  const subjectRules = [
    ['学习理论', /泛化|标度律|Scaling Laws|Learning Theory|Deep Learning Theory|In.Context Learning|Neural Scaling|Compositional|Length Generalization|AI Theory|Physics of AI|physics of AI|Physics of Deep Learning|^Theory$/i],
    ['优化与训练', /优化|训练|Training|Optimization|Initialization|Signal Propagation|Grokking|Lottery Tickets|Transformer Dynamics/i],
    ['表示与可解释性', /表示学习|可解释性|Representation|Interpretability|Explainable|Model Analysis|Neurosymbolic|Symbolic Reasoning|Modular Networks|Compositionality/i],
    ['语言模型', /语言模型|Transformer|Language Model|LLM|Prompting/i],
    ['生成模型', /生成模型|Generative|Flow Matching|Diffusion|Video Generation/i],
    ['强化学习与控制', /强化学习|Reinforcement|Control|World Models|世界模型|AI Agents|LLM Agents/i],
    ['科学机器学习', /AI for Science|AI for Physics|Scientific|神经算子|Neural Operators|计算物理|物理数据分析|Symbolic Regression|Reduced.Order Modeling/i],
    ['统计物理', /统计物理|相变|临界|无序系统|Spin Glass|Ising|低温刚性|关联恒等式|Renormalization Group|Statistical Physics|Statistical Mechanics|Statistical mechanics|Mean.field Phase Transitions/i],
    ['活性与软物质', /活性物质|Active Matter|软物质|Soft Matter|Nonreciprocal/i],
    ['流体物理', /流体|水动力学|Fluid Dynamics|Hydrodynamic|Climate Dynamics/i],
    ['生物与神经', /生物|神经动力学|神经计算|Neuroscience|NeuroAI|Learning Dynamics and Neuroscience/i],
    ['凝聚态物理', /凝聚态|强关联|Condensed Matter|Photonic Computing|Thermodynamic Computing/i],
    ['场论与高能', /场论|高能|Field Theory/i],
    ['对称性与几何', /对称性与规范|Representation Theory|Representation Geometry|Geometric/i],
    ['概率与数学', /概率|随机过程|随机动力学|Information Theory|数学物理|Mathematical Physics|应用数学|数值分析|浓缩不等式|整数高度场|Random Matrix/i],
    ['非线性与复杂系统', /非线性|混沌|动力系统|Complex Systems|Dynamical Systems|动力学相变|弱噪声极限/i],
    ['量子物理', /量子|Quantum Physics/i],
    ['机器人与具身智能', /机器人|具身智能|Robotics/i],
    ['视觉与感知', /计算机视觉|Computer Vision/i],
    ['机器学习', /^机器学习$|^人工智能$|^Machine Learning$|^Efficient AI$/i],
    ['跨学科', /^跨学科$/i]
  ];
  function readerTags(tags){
    const subjects = subjectRules.filter(([, pattern]) => tags.some(tag => pattern.test(tag))).map(([name]) => name);
    // Broad AI labels add little when a paper already has a specific subject.
    return subjects.length > 1 ? subjects.filter(tag => tag !== '机器学习') : subjects;
  }

  function buildSearchText(item){
    return [
      item.title || '',
      item.authors || '',
      item.title_zh || '',
      item.preview_text || '',
      item.research_unit || '',
      item.arxiv_id || '',
      item.hook_text || '',
      item.category || '',
      item.research_type || '',
      ...(item.originalTags || item.tags || []),
      ...(item.arxiv_categories || []),
      ...(item.key_points || [])
    ].join(' ').toLowerCase();
  }

  let mathQueue = Promise.resolve();
  function typesetSurface(element){
    const math = window.MathJax;
    if(!math || !math.startup) return;
    mathQueue = mathQueue.then(() => math.startup.promise).then(() => {
      if(element.isConnected && math.typesetPromise) return math.typesetPromise([element]).then(() => window.fitInlineMath?.(element));
    }).catch(error => console.error('公式排版失败', error));
  }

  function createFeedCard(item){
    const cardShell = document.createElement('div');
    cardShell.className = 'feed-card-shell';

    const cardLink = document.createElement('a');
    cardLink.className = 'feed-card-link';
    cardLink.href = item.detail_path;
    cardLink.setAttribute('aria-label', `查看论文：${item.title}`);
    cardLink.setAttribute('aria-haspopup', 'dialog');
    cardLink.addEventListener('pointerdown', saveCatalogReturnURL);
    cardLink.addEventListener('auxclick', saveCatalogReturnURL);
    cardLink.addEventListener('contextmenu', saveCatalogReturnURL);
    cardLink.addEventListener('click', (event) => {
      saveCatalogReturnURL();
      const shouldUseNormalNavigation = event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;
      if(shouldUseNormalNavigation){
        return;
      }
      event.preventDefault();
      openPaperModal(item, { updateHistory: true, returnFocus: cardLink });
    });

    const card = document.createElement('article');
    card.className = 'feed-card';

    const coverWrap = document.createElement('div');
    coverWrap.className = 'feed-card-cover';
    const imagePath = item.paper_image_path || item.fallback_image_path || '';
    if(imagePath){
      const figure = document.createElement('figure');
      figure.className = 'feed-card-figure';

      const image = document.createElement('img');
      image.className = 'paper-figure-image';
      image.src = imagePath;
      image.alt = item.cover_alt_text || item.title || '论文封面图';
      image.loading = 'lazy';
      image.dataset.zoomable = 'true';
      image.tabIndex = 0;
      image.setAttribute('role', 'button');
      image.setAttribute('aria-label', `放大图片：${item.title || '论文'}`);
      image.addEventListener('keydown', event => {
        if(event.key === 'Enter' || event.key === ' '){
          event.preventDefault();
          event.stopPropagation();
          openPaperImage(item, image);
        }
      });
      image.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        openPaperImage(item, image);
      });

      figure.appendChild(image);
      coverWrap.appendChild(figure);
    } else {
      const cover = document.createElement('div');
      cover.className = 'note-cover note-cover-feed note-cover-title-abstract';
      applyCoverTheme(cover, item.cover_theme);

      const mesh = document.createElement('div');
      mesh.className = 'note-cover-mesh';
      cover.appendChild(mesh);

      const titleShell = document.createElement('div');
      titleShell.className = 'note-cover-title-shell';

      const kicker = document.createElement('span');
      kicker.className = 'note-cover-kicker';
      kicker.textContent = 'TITLE · ABSTRACT';
      titleShell.appendChild(kicker);

      const title = document.createElement('h3');
      title.className = 'note-cover-title';
      title.textContent = item.title;
      titleShell.appendChild(title);

      const abstractText = document.createElement('p');
      abstractText.className = 'note-cover-abstract';
      abstractText.textContent = item.preview_text || '暂无摘要';
      titleShell.appendChild(abstractText);
      cover.appendChild(titleShell);
      coverWrap.appendChild(cover);
    }

    const cardBody = document.createElement('div');
    cardBody.className = 'feed-card-body';

    const meta = document.createElement('div');
    meta.className = 'feed-card-meta';

    [...new Set([...(item.tags || []).slice(0, 3), item.grade].filter(Boolean))].forEach(value => {
      const tag = document.createElement('span');
      tag.className = 'feed-chip feed-chip-tag';
      tag.textContent = value;
      meta.appendChild(tag);
    });

    const bodyTitle = document.createElement('div');
    bodyTitle.className = 'feed-card-title';
    bodyTitle.textContent = item.title || '未命名论文';

    const bodyTitleZh = document.createElement('div');
    bodyTitleZh.className = 'feed-card-title-zh';
    bodyTitleZh.textContent = item.title_zh || '';

    const preview = document.createElement('div');
    preview.className = 'feed-card-preview';
    preview.textContent = item.preview_text || '暂无摘要';

    const footer = document.createElement('div');
    footer.className = 'feed-card-footer';

    const action = document.createElement('div');
    action.className = 'feed-card-action';
    action.textContent = '打开阅读卡';

    const stats = document.createElement('div');
    stats.className = 'feed-card-stats';
    stats.textContent = `约 ${item.reading_minutes || 1} 分钟`;

    footer.appendChild(action);
    footer.appendChild(stats);

    if(meta.childNodes.length){
      cardBody.appendChild(meta);
    }
    cardBody.appendChild(bodyTitle);
    if(item.title_zh){
      cardBody.appendChild(bodyTitleZh);
    }
    cardBody.appendChild(preview);
    cardBody.appendChild(footer);

    card.appendChild(coverWrap);
    card.appendChild(cardBody);
    cardLink.appendChild(card);

    const favoriteButton = document.createElement('button');
    const favorite = isFavorite(item);
    favoriteItems.set(favoriteButton, item);
    favoriteButton.type = 'button';
    favoriteButton.className = 'feed-favorite-button';
    favoriteButton.textContent = favorite ? '★' : '☆';
    favoriteButton.setAttribute('aria-pressed', String(favorite));
    favoriteButton.setAttribute('aria-label', `${favorite ? '取消收藏' : '收藏'}：${item.title || '论文'}`);
    favoriteButton.title = favorite ? '取消收藏' : '收藏';
    favoriteButton.addEventListener('click', () => toggleFavorite(item));

    cardShell.appendChild(cardLink);
    cardShell.appendChild(favoriteButton);
    return cardShell;
  }

  function createGroupSection(date, items){
    const section = document.createElement('section');
    section.className = 'group';

    const heading = document.createElement('div');
    heading.className = 'group-heading';

    const h2 = document.createElement('h2');
    h2.textContent = date;

    const count = document.createElement('div');
    count.className = 'group-count';
    count.textContent = `${items.length} 篇`;

    const grid = document.createElement('div');
    grid.className = 'grid';

    items.forEach((item) => {
      grid.appendChild(createFeedCard(item));
    });

    heading.appendChild(h2);
    heading.appendChild(count);
    section.appendChild(heading);
    if(items.length) section.appendChild(grid);
    else {
      const empty = document.createElement('p');
      empty.className = 'group-empty empty-day';
      empty.textContent = state.q || state.tag || state.grade !== 'all' ? '这一天没有匹配的论文。' : '这一天没有收录论文。';
      section.appendChild(empty);
    }
    return section;
  }

  const DAY_MS = 86400000;
  const textCompare = (a, b) => String(a || '').localeCompare(String(b || ''), 'zh-CN');

  // UTC arithmetic avoids DST changes; only real calendar dates are accepted.
  function dayNumber(value){
    const match = /^(\d{4})-(\d{2})-(\d{2})(?:$|[T\s])/.exec(String(value || ''));
    if(!match) return null;
    const iso = `${match[1]}-${match[2]}-${match[3]}`;
    const time = Date.parse(`${iso}T00:00:00Z`);
    return Number.isFinite(time) && new Date(time).toISOString().slice(0, 10) === iso ? time / DAY_MS : null;
  }

  function collectionDay(item){ return dayNumber(item.collection_date); }
  function publishedDay(item){
    const value = String(item.published || '');
    // Partial publication dates remain known dates: sort at the start of their
    // stated year/month, without inventing precision in the record or label.
    if(/^\d{4}$/.test(value)) return dayNumber(`${value}-01-01`);
    if(/^\d{4}-\d{2}$/.test(value)) return dayNumber(`${value}-01`);
    return dayNumber(value);
  }
  function descendingDay(a, b){
    if(a === b) return 0;
    if(a === null) return 1;
    if(b === null) return -1;
    return b - a;
  }
  function stableRecordCompare(a, b){
    return descendingDay(collectionDay(a), collectionDay(b)) ||
      descendingDay(publishedDay(a), publishedDay(b)) || textCompare(a.title, b.title) ||
      textCompare(a.arxiv_id || a.detail_path, b.arxiv_id || b.detail_path);
  }
  function categoryName(item){ return item.category || '未分类'; }

  function filterItems(){
    const tokens = state.q.trim().toLowerCase().split(/\s+/).filter(Boolean).map(value => value.replace(/[-_]/g, ''));
    return DATA.filter(item => {
      if(state.tag && !item.tags.includes(state.tag) && !item.originalTags.includes(state.tag)) return false;
      if(state.grade !== 'all' && item.grade !== state.grade) return false;
      const haystack = buildSearchText(item).replace(/[-_]/g, '');
      return tokens.every(token => haystack.includes(token));
    });
  }

  function readURLState(){
    const params = new URL(window.location.href).searchParams;
    const page = Number(params.get('page') || 1);
    state = {
      mode: ['daily', 'published', 'category'].includes(params.get('mode')) ? params.get('mode') : 'daily',
      page: Number.isSafeInteger(page) && page > 0 ? page : 1,
      tag: params.get('tag') || '',
      grade: ['S', 'A', 'B'].includes(params.get('grade')) ? params.get('grade') : 'all',
      q: params.get('q') || ''
    };
    // Preserve even a retired tag in a shared link, so it produces an honest
    // empty result instead of silently broadening the filter.
    if(state.tag && !Array.from(tagFilterEl.options).some(option => option.value === state.tag)){
      tagFilterEl.add(new Option(state.tag, state.tag));
    }
    searchEl.value = state.q;
    modeEl.value = state.mode;
    gradeEl.value = state.grade;
    tagFilterEl.value = state.tag;
  }

  function writeURLState(replace){
    const url = new URL(window.location.href);
    Object.entries(state).forEach(([key, value]) => {
      if(value === '' || (key === 'grade' && value === 'all')) url.searchParams.delete(key);
      else url.searchParams.set(key, String(value));
    });
    if(url.href === window.location.href) return;
    const previous = window.history.state && typeof window.history.state === 'object' ? window.history.state : {};
    window.history[replace ? 'replaceState' : 'pushState']({...previous}, '', url);
  }

  function goToPage(page){
    state.page = page;
    writeURLState(false);
    sync();
    groupsEl.scrollIntoView({block: 'start'});
  }

  function renderPagination(totalPages){
    paginationEl.replaceChildren();
    paginationEl.setAttribute('aria-label', '论文分页');
    const button = (label, page, disabled = false) => {
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'pagination-button';
      el.textContent = label;
      el.disabled = disabled;
      el.addEventListener('click', () => goToPage(page));
      return el;
    };
    paginationEl.appendChild(button('首页', 1, state.page <= 1));
    paginationEl.appendChild(button('上一页', state.page - 1, state.page <= 1));
    const start = Math.max(1, Math.min(state.page - 2, totalPages - 4));
    for(let page = start; page <= Math.min(totalPages, start + 4); page++){
      const el = button(String(page), page);
      el.setAttribute('aria-label', `第 ${page} 页`);
      if(page === state.page) el.setAttribute('aria-current', 'page');
      paginationEl.appendChild(el);
    }
    paginationEl.appendChild(button('下一页', state.page + 1, state.page >= totalPages));
    paginationEl.appendChild(button('尾页', totalPages, state.page >= totalPages));
    const jumpLabel = document.createElement('label');
    jumpLabel.className = 'page-jump';
    jumpLabel.textContent = '跳转到';
    const select = document.createElement('select');
    select.id = 'page-select';
    select.setAttribute('aria-label', '选择页码');
    for(let page = 1; page <= totalPages; page++) select.add(new Option(`第 ${page} 页`, String(page)));
    select.value = String(state.page);
    select.addEventListener('change', () => goToPage(Number(select.value)));
    jumpLabel.appendChild(select);
    paginationEl.appendChild(jumpLabel);
    const label = document.createElement('span');
    label.className = 'pagination-info page-summary';
    label.setAttribute('aria-live', 'polite');
    label.textContent = `第 ${state.page} / ${totalPages} 页` + (state.mode === 'daily' ? ' · 每页 5 天' : ` · 每页 ${catalogPageSize} 篇`);
    paginationEl.appendChild(label);
  }

  let catalogPageSize = 10;
  function measurePageSize(){
    const probe = document.createElement('div');
    probe.className = 'grid';
    probe.style.cssText = 'height:0;visibility:hidden;overflow:hidden';
    groupsEl.appendChild(probe);
    const columns = Math.max(1, getComputedStyle(probe).gridTemplateColumns.split(/\s+/).filter(Boolean).length);
    probe.remove();
    return Math.ceil(10 / columns) * columns;
  }

  function renderGroups(items){
    if(window.MathJax?.typesetClear) window.MathJax.typesetClear([groupsEl]);
    groupsEl.replaceChildren();
    let totalPages;
    if(state.mode === 'daily'){
      const timeline = state.q || state.tag || state.grade !== 'all' ? items : DATA;
      const dates = timeline.map(collectionDay).filter(day => day !== null);
      const latest = dates.length ? dates.reduce((a, b) => Math.max(a, b)) : null;
      const earliest = dates.length ? dates.reduce((a, b) => Math.min(a, b)) : null;
      const calendarPages = dates.length ? Math.ceil((latest - earliest + 1) / 5) : 0;
      const hasUndated = timeline.some(item => collectionDay(item) === null);
      totalPages = Math.max(1, calendarPages + Number(hasUndated));
      state.page = Math.min(state.page, totalPages);
      if(state.page <= calendarPages){
        const first = latest - (state.page - 1) * 5;
        for(let offset = 0; offset < 5; offset++){
          const day = first - offset;
          const records = items.filter(item => collectionDay(item) === day).sort(stableRecordCompare);
          groupsEl.appendChild(createGroupSection(new Date(day * DAY_MS).toISOString().slice(0, 10), records));
        }
      } else if(hasUndated){
        groupsEl.appendChild(createGroupSection('收录日期未知', items.filter(item => collectionDay(item) === null).sort(stableRecordCompare)));
      }
    } else {
      const sorted = items.slice().sort(state.mode === 'published'
        ? (a, b) => descendingDay(publishedDay(a), publishedDay(b)) || stableRecordCompare(a, b)
        : (a, b) => textCompare(categoryName(a), categoryName(b)) || stableRecordCompare(a, b));
      totalPages = Math.max(1, Math.ceil(sorted.length / catalogPageSize));
      state.page = Math.min(state.page, totalPages);
      const pageItems = sorted.slice((state.page - 1) * catalogPageSize, state.page * catalogPageSize);
      if(state.mode === 'category'){
        const groups = new Map();
        pageItems.forEach(item => {
          const category = categoryName(item);
          if(!groups.has(category)) groups.set(category, []);
          groups.get(category).push(item);
        });
        groups.forEach((records, category) => groupsEl.appendChild(createGroupSection(category, records)));
      } else if(pageItems.length){
        groupsEl.appendChild(createGroupSection('按发表日期', pageItems));
      }
    }
    renderPagination(totalPages);
    // Normalize an invalid/out-of-range page without adding another history entry.
    writeURLState(true);
    typesetSurface(groupsEl);
  }

  function sync(){
    if(!loaded) return;
    catalogPageSize = measurePageSize();
    const items = filterItems();
    paperCountEl.textContent = state.q || state.tag || state.grade !== 'all'
      ? `${items.length} / ${DATA.length} 篇` : `${DATA.length} 篇已收录`;
    renderGroups(items);
    if(!DATA.length){
      renderStatus('empty', '还没有论文卡片', '暂时没有可展示的论文。');
    } else if(!items.length){
      renderStatus('empty', '没有找到匹配卡片', '试试其他关键词、标签或等级。', {
        label: '清空筛选', onClick: () => {
          state = {...state, page: 1, q: '', tag: '', grade: 'all'};
          writeURLState(false);
          readURLState();
          sync();
          searchEl.focus();
        }
      });
    } else clearStatus();
  }

  function controlsChanged(){
    state = {mode: modeEl.value, page: 1, q: searchEl.value, tag: tagFilterEl.value, grade: gradeEl.value};
    writeURLState(false);
    sync();
  }
  searchEl.addEventListener('input', controlsChanged);
  [modeEl, tagFilterEl, gradeEl].forEach(el => el.addEventListener('change', controlsChanged));
  window.addEventListener('popstate', () => {
    readURLState();
    sync();
    openPaperModalFromURL();
  });
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if(!loaded || state.mode === 'daily') return;
      const nextSize = measurePageSize();
      if(nextSize === catalogPageSize) return;
      state.page = Math.floor((state.page - 1) * catalogPageSize / nextSize) + 1;
      sync();
    }, 160);
  });
  window.addEventListener('storage', event => {
    if(event.key === favoritesStorageKey || event.key === null) refreshFavorites();
  });

  window.addEventListener('message', event => {
    if(event.origin !== window.location.origin || !paperModalFrameEl || event.source !== paperModalFrameEl.contentWindow) return;
    const message = event.data || {};
    if(message.type === 'paper-modal-close') requestClosePaperModal();
    if(message.type === 'paper-modal-ready' && paperModalEl?.classList.contains('is-open')){
      if(message.title){
        if(window.MathJax?.typesetClear) window.MathJax.typesetClear([paperModalTitleEl]);
        paperModalTitleEl.textContent = message.title;
        typesetSurface(paperModalTitleEl);
      }
      if(message.url){
        try {
          const url = new URL(message.url, window.location.href);
          if(url.origin === window.location.origin){
            url.searchParams.delete('embed');
            paperModalOpenLinkEl.href = url.href;
            const destination = DATA.find(item => [item.detail_path, ...(item.source_records || []).map(record => record.detail_path)].some(path => new URL(path, window.location.href).pathname === url.pathname));
            if(destination){
              openIdentifier = getPaperIdentifier(destination);
              const catalogURL = new URL(window.location.href);
              catalogURL.searchParams.set(paperModalQueryKey, openIdentifier);
              const ownedState = window.history.state || {};
              window.history.replaceState({...ownedState, ...(ownedState.paperModal ? {paperModal: openIdentifier} : {})}, '', catalogURL);
            }
          }
        } catch(error){ console.warn('无效的论文地址', error); }
      }
    }
    if(message.type === 'paper-favorite-changed') refreshFavorites(message.key);
    if(message.type === 'paper-image-open' && window.PaperImageViewer){
      window.PaperImageViewer.open({src: message.src, alt: message.alt || '论文图片', caption: message.caption || message.alt || ''});
    }
  });

  window.addEventListener('keydown', event => {
    if(event.defaultPrevented) return;
    // Handle the lightbox first even on its first open (its listener is lazy).
    if(event.key === 'Escape' && window.PaperImageViewer?.isOpen()){
      event.preventDefault();
      window.PaperImageViewer.close();
      return;
    }
    if(!paperModalEl?.classList.contains('is-open')) return;
    if(event.key === 'Escape'){
      event.preventDefault();
      requestClosePaperModal();
    } else if(event.key === 'Tab' && !window.PaperImageViewer?.isOpen()){
      const first = paperModalOpenLinkEl;
      const last = paperModalFrameEl;
      if(event.shiftKey && document.activeElement === first){ event.preventDefault(); last.focus(); }
      else if(!event.shiftKey && document.activeElement === last){ event.preventDefault(); first.focus(); }
    }
  });

  let loading = false;
  async function loadData(){
    if(loading) return;
    loading = true;
    renderStatus('loading', '正在加载论文卡片', '正在读取论文列表。');
    try {
      const response = await fetch('assets/all-data.json');
      if(!response.ok) throw new Error(`HTTP ${response.status}`);
      const records = await response.json();
      if(!Array.isArray(records)) throw new Error('论文数据应为数组');
      DATA = records.filter(item => item && typeof item === 'object' && typeof item.detail_path === 'string' && item.detail_path)
        .map(item => {
          const originalTags = Array.isArray(item.tags) ? item.tags.filter(tag => typeof tag === 'string' && tag) : [];
          return {...item, originalTags, tags: readerTags(originalTags)};
        });
      const selectedTag = new URL(window.location.href).searchParams.get('tag') || '';
      tagFilterEl.replaceChildren(new Option('全部标签', ''));
      const tags = [...new Set(DATA.flatMap(item => item.tags))].sort(textCompare);
      tags.forEach(tag => tagFilterEl.add(new Option(tag, tag)));
      if(selectedTag && !tags.includes(selectedTag)) tagFilterEl.add(new Option(selectedTag, selectedTag));
      loaded = true;
      readURLState();
      sync();
      openPaperModalFromURL();
    } catch(error){
      console.error('论文列表加载失败', error);
      loaded = false;
      groupsEl.replaceChildren();
      paginationEl.replaceChildren();
      paperCountEl.textContent = '暂无法读取论文数量';
      renderStatus('error', '论文卡片加载失败', '无法读取论文列表，请稍后重试。', {label: '重新加载', onClick: loadData});
    } finally { loading = false; }
  }

  readURLState();
  loadData();
})();
