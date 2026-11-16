(function () {
  // ---- theme toggle
  var root = document.documentElement;
  var btn = document.getElementById('theme-btn');
  if (btn) btn.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme');
    if (!cur) cur = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('cv-theme', next); } catch (e) {}
  });

  // ---- search
  var input = document.getElementById('search');
  var box = document.getElementById('search-results');
  var index = window.SEARCH_INDEX || [];
  var sel = -1;
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function mark(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      if (!t) return;
      out = out.replace(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), function (m) { return '<mark>' + m + '</mark>'; });
    });
    return out;
  }
  function search(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    var res = [];
    index.forEach(function (p) {
      var t = p.t.toLowerCase(), x = p.x.toLowerCase(), score = 0, ok = true;
      terms.forEach(function (term) {
        var inT = t.indexOf(term) >= 0, inX = x.indexOf(term);
        if (!inT && inX < 0) ok = false;
        score += (inT ? 10 : 0) + (inX >= 0 ? 1 : 0);
      });
      if (!ok) return;
      var pos = x.indexOf(terms[0]);
      var snip = pos >= 0 ? p.x.substr(Math.max(0, pos - 40), 120) : p.x.substr(0, 110);
      res.push({ p: p, score: score, snip: (pos > 40 ? '…' : '') + snip + '…' });
    });
    res.sort(function (a, b) { return b.score - a.score; });
    return res.slice(0, 12).map(function (r) { r.terms = terms; return r; });
  }
  function draw() {
    var q = input.value.trim();
    if (!q) { box.hidden = true; return; }
    var res = search(q);
    sel = -1;
    box.innerHTML = res.length ? res.map(function (r) {
      return '<a href="' + r.p.s + '.html"><span class="r-title">' + mark(r.p.t, r.terms) + '</span><span class="r-cat">' + esc(r.p.c) +
        '</span><div class="r-snip">' + mark(r.snip, r.terms) + '</div></a>';
    }).join('') : '<div class="empty">검색 결과가 없습니다.</div>';
    box.hidden = false;
  }
  if (input) {
    input.addEventListener('input', draw);
    input.addEventListener('focus', draw);
    input.addEventListener('keydown', function (e) {
      var links = box.querySelectorAll('a');
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (!links.length) return;
        sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
        links.forEach(function (a, i) { a.classList.toggle('sel', i === sel); });
      } else if (e.key === 'Enter') {
        var a = links[sel >= 0 ? sel : 0];
        if (a) location.href = a.getAttribute('href');
      } else if (e.key === 'Escape') { box.hidden = true; input.blur(); }
    });
    document.addEventListener('click', function (e) { if (!e.target.closest('.search')) box.hidden = true; });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== input && !/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); input.focus(); }
    });
  }

  // ---- toc highlight
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('on'); });
          var a = map[en.target.id]; if (a) a.classList.add('on');
        }
      });
    }, { rootMargin: '-70px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) obs.observe(el); });
  }

  // ---- broken image fallback
  document.querySelectorAll('article img').forEach(function (img) {
    img.addEventListener('error', function () { var a = img.closest('.img-link'); if (a) a.style.display = 'none'; });
  });

  // ---- spawn list
  if (window.PAGE_DATA && document.getElementById('spawn-app')) spawnApp(window.PAGE_DATA);

  function spawnApp(data) {
    var app = document.getElementById('spawn-app');
    var gens = [];
    data.forEach(function (d) { if (gens.indexOf(d.g) < 0) gens.push(d.g); });
    var models = {};
    data.forEach(function (d) { models[d.m] = 1; });
    app.innerHTML =
      '<div class="filters">' +
      '<input id="f-q" type="search" placeholder="포켓몬 이름, 번호, 바이옴 검색 (한/영)">' +
      '<select id="f-g"><option value="">전체 세대</option>' + gens.map(function (g) { return '<option>' + esc(g) + '</option>'; }).join('') + '</select>' +
      '<select id="f-r"><option value="">전체 희귀도</option><option value="common">흔함</option><option value="uncommon">드묾</option><option value="rare">희귀</option><option value="ultra">초희귀</option></select>' +
      '<select id="f-m"><option value="">전체 모델 출처</option>' + Object.keys(models).sort().map(function (m) { return '<option>' + esc(m) + '</option>'; }).join('') + '</select>' +
      '<label><input id="f-o" type="checkbox"> 영문 원문 표시</label>' +
      '</div><div class="count" id="f-count"></div>' +
      '<div class="table-wrap"><table class="spawn-table" id="f-table"><thead><tr><th>No.</th><th>포켓몬</th><th>희귀도</th><th>스폰 위치</th><th>조건</th><th>폼 / 기타</th><th>모델</th><th class="orig">원문</th></tr></thead><tbody></tbody></table></div>' +
      '<button class="more-btn" id="f-more" hidden>더 보기</button>';
    var q = document.getElementById('f-q'), g = document.getElementById('f-g'), r = document.getElementById('f-r'),
      m = document.getElementById('f-m'), o = document.getElementById('f-o'), tb = document.querySelector('#f-table tbody'),
      cnt = document.getElementById('f-count'), more = document.getElementById('f-more'), table = document.getElementById('f-table');
    var limit = 150, rows = [];
    function rarityClass(rk) { return { common: 'r-common', uncommon: 'r-uncommon', rare: 'r-rare', ultra: 'r-ultra' }[rk] || ''; }
    function filter() {
      var terms = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      rows = data.filter(function (d) {
        if (g.value && d.g !== g.value) return false;
        if (r.value && d.rk.indexOf(r.value) < 0) return false;
        if (m.value && d.m !== m.value) return false;
        var hay = (d.n + ' ' + d.ko + ' ' + d.en + ' ' + d.s + ' ' + d.c + ' ' + d.f + ' ' + d.os + ' ' + d.oc + ' ' + d.of).toLowerCase();
        return terms.every(function (t) { return hay.indexOf(t) >= 0; });
      });
      paint();
    }
    function paint() {
      var shown = rows.slice(0, limit);
      tb.innerHTML = shown.map(function (d) {
        return '<tr><td class="num">' + esc(d.n) + '</td><td class="name">' + esc(d.ko) + '<small>' + esc(d.en) + '</small></td>' +
          '<td>' + (d.r ? '<span class="badge ' + rarityClass(d.rk[0]) + '">' + esc(d.r) + '</span>' : '') + '</td>' +
          '<td>' + esc(d.s) + '</td><td>' + esc(d.c) + '</td><td>' + esc(d.f) + '</td><td>' + esc(d.m) + '</td>' +
          '<td class="orig">' + esc([d.os, d.oc, d.of].filter(Boolean).join(' / ')) + '</td></tr>';
      }).join('');
      cnt.textContent = '총 ' + rows.length + '마리' + (rows.length > limit ? ' 중 ' + limit + '마리 표시' : '');
      more.hidden = rows.length <= limit;
    }
    more.addEventListener('click', function () { limit += 300; paint(); });
    [q, g, r, m].forEach(function (el) { el.addEventListener('input', function () { limit = 150; filter(); }); });
    o.addEventListener('change', function () { table.classList.toggle('show-orig', o.checked); });
    var hash = decodeURIComponent(location.hash.slice(1));
    if (hash) q.value = hash;
    filter();
  }
})();
