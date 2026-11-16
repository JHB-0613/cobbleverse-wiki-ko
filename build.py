"""COBBLEVERSE 한국어 위키 빌드 스크립트.

src/pages/*.md (한국어 원고) -> site/*.html (정적 사이트)
사용법:  python build.py
"""
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
PAGES = os.path.join(SRC, 'pages')
OUT = os.path.join(ROOT, 'site')

CATEGORIES = [
    ('install', '설치', '📥'),
    ('gameplay', '게임플레이', '🎮'),
    ('tutorials', '공략 · 튜토리얼', '🧭'),
    ('issues', '자주 묻는 문제', '🛠️'),
    ('gyms', '체육관 관장', '🏅'),
    ('settings', '설정', '⚙️'),
    ('changelogs', '업데이트 기록', '📜'),
]


# ---------------------------------------------------------------- markdown
def slugify(text):
    s = re.sub(r'<[^>]+>', '', text)
    s = re.sub(r'[^\w\s가-힣-]', '', s).strip().lower()
    return re.sub(r'\s+', '-', s) or 'section'


def inline(text):
    """인라인 마크다운: 코드, 이미지, 링크, 굵게, 기울임."""
    codes = []

    def keep_code(m):
        codes.append('<code>' + html.escape(m.group(1)) + '</code>')
        return '\x00%d\x00' % (len(codes) - 1)

    text = re.sub(r'`([^`]+)`', keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', lambda m: img_tag(m.group(2), m.group(1)), text)

    def link(m):
        label, href = m.group(1), m.group(2)
        if href.startswith('http'):
            return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, label)
        page, hashpart = (href.split('#', 1) + [''])[:2] if '#' in href else (href, None)
        if page and not page.endswith('.html') and not page.startswith('/'):
            page += '.html'
        href = page + ('#' + hashpart if hashpart is not None else '')
        return '<a href="%s">%s</a>' % (href, label)

    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', text)
    text = re.sub(r'\x00(\d+)\x00', lambda m: codes[int(m.group(1))], text)
    return text


def img_tag(src, alt=''):
    if src.startswith('up:'):  # 원본 위키 업로드 폴더 단축 표기
        src = 'https://www.lumyverse.com/wp-content/uploads/' + src[3:]
    return ('<a class="img-link" href="%s" target="_blank" rel="noopener"><img src="%s" alt="%s" '
            'loading="lazy" referrerpolicy="no-referrer"></a>') % (src, src, html.escape(alt))


def md_to_html(md):
    lines = md.split('\n')
    out, toc = [], []
    i = 0
    used_ids = set()

    def heading_id(text):
        base = slugify(text)
        hid, n = base, 2
        while hid in used_ids:
            hid = '%s-%d' % (base, n)
            n += 1
        used_ids.add(hid)
        return hid

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        # code block
        if s.startswith('```'):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append('<pre><code>%s</code></pre>' % html.escape('\n'.join(buf)))
            continue
        # raw html block (줄이 '<'로 시작하면 빈 줄까지 그대로 출력)
        if s.startswith('<'):
            buf = []
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i])
                i += 1
            out.append('\n'.join(buf))
            continue
        # heading
        m = re.match(r'^(#{1,4})\s+(.*)$', s)
        if m:
            level = len(m.group(1))
            txt = inline(m.group(2))
            hid = heading_id(m.group(2))
            if level in (2, 3):
                toc.append((level, hid, re.sub(r'<[^>]+>', '', txt)))
            out.append('<h%d id="%s">%s</h%d>' % (level, hid, txt, level))
            i += 1
            continue
        # callout
        if s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            kind = 'note'
            m = re.match(r'^\[!(\w+)\]\s*(.*)$', buf[0])
            if m:
                kind = m.group(1).lower()
                buf[0] = m.group(2)
            labels = {'note': '참고', 'tip': '팁', 'warning': '주의', 'important': '중요'}
            body, items = '', []
            for b in buf + ['']:
                if b.startswith('- '):
                    items.append('<li>%s</li>' % inline(b[2:]))
                    continue
                if items:
                    body += '<ul>%s</ul>' % ''.join(items)
                    items = []
                if b:
                    body += '<p>%s</p>' % inline(b)
            out.append('<div class="callout callout-%s"><div class="callout-title">%s</div>%s</div>'
                       % (kind, labels.get(kind, '참고'), body))
            continue
        # table
        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
            if len(cells) > 1 and all(re.match(r'^:?-{2,}:?$', c) for c in cells[1] if c):
                cells.pop(1)
            head, body = cells[0], cells[1:]
            t = ['<div class="table-wrap"><table><thead><tr>']
            t += ['<th>%s</th>' % inline(c) for c in head]
            t.append('</tr></thead><tbody>')
            for r in body:
                t.append('<tr>' + ''.join('<td>%s</td>' % inline(c) for c in r) + '</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            continue
        # image gallery (consecutive image-only lines)
        if re.match(r'^!\[[^\]]*\]\([^)]+\)$', s):
            imgs = []
            while i < len(lines) and re.match(r'^!\[[^\]]*\]\([^)]+\)$', lines[i].strip()):
                m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', lines[i].strip())
                imgs.append(img_tag(m.group(2), m.group(1)))
                i += 1
            cls = 'gallery single' if len(imgs) == 1 else 'gallery'
            out.append('<div class="%s">%s</div>' % (cls, ''.join(imgs)))
            continue
        # list
        if re.match(r'^(\s*)([-*]|\d+\.)\s+', line):
            ordered = re.match(r'^\s*(\d+)\.', line)
            tag = 'ol' if ordered else 'ul'
            if ordered and ordered.group(1) != '1':
                tag_open = 'ol start="%s"' % ordered.group(1)
            else:
                tag_open = tag
            items = []
            while i < len(lines) and re.match(r'^(\s*)([-*]|\d+\.)\s+', lines[i]):
                m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', lines[i])
                items.append((len(m.group(1)), m.group(3)))
                i += 1
            html_items, open_sub = [], False
            for indent, txt in items:
                if indent >= 2:
                    if not open_sub:
                        html_items[-1] = html_items[-1][:-5] + '<ul>'
                        open_sub = True
                    html_items.append('<li>%s</li>' % inline(txt))
                else:
                    if open_sub:
                        html_items.append('</ul></li>')
                        open_sub = False
                    html_items.append('<li>%s</li>' % inline(txt))
            if open_sub:
                html_items.append('</ul></li>')
            out.append('<%s>%s</%s>' % (tag_open, ''.join(html_items), tag))
            continue
        # paragraph
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(#{1,4}\s|>|\||```|!\[|\s*([-*]|\d+\.)\s)', lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        if not buf:  # safety
            buf.append(s)
            i += 1
        out.append('<p>%s</p>' % inline(' '.join(buf)))
    return '\n'.join(out), toc


# ---------------------------------------------------------------- pages
def read_page(path):
    raw = open(path, encoding='utf-8').read()
    meta = {}
    m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
    if m:
        for ln in m.group(1).split('\n'):
            if ':' in ln:
                k, v = ln.split(':', 1)
                meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    meta['slug'] = os.path.splitext(os.path.basename(path))[0]
    meta['order'] = int(meta.get('order', 99))
    meta['body'] = raw
    return meta


def plain_text(md):
    t = re.sub(r'!\[[^\]]*\]\([^)]+\)', ' ', md)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'[#>*`|]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def sidebar(pages, current):
    parts = []
    for key, label, icon in CATEGORIES:
        items = [p for p in pages if p.get('category') == key]
        if not items:
            continue
        open_attr = ' open' if any(p['slug'] == current for p in items) or current == 'index' else ''
        parts.append('<details class="nav-group"%s><summary><span class="nav-icon">%s</span>%s</summary><ul>'
                     % (open_attr, icon, label))
        for p in sorted(items, key=lambda x: x['order']):
            cls = ' class="active"' if p['slug'] == current else ''
            parts.append('<li><a%s href="%s.html">%s</a></li>' % (cls, p['slug'], html.escape(p['title'])))
        parts.append('</ul></details>')
    return '\n'.join(parts)


def render(template, **kw):
    for k, v in kw.items():
        template = template.replace('{{%s}}' % k, v)
    return template


def main():
    pages = [read_page(os.path.join(PAGES, f)) for f in sorted(os.listdir(PAGES)) if f.endswith('.md')]
    template = open(os.path.join(SRC, 'template.html'), encoding='utf-8').read()
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):  # 폴더는 남기고 내용만 비움 (미리보기 서버가 폴더를 잡고 있어도 동작)
        p = os.path.join(OUT, f)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    for f in os.listdir(os.path.join(SRC, 'assets')):
        shutil.copy(os.path.join(SRC, 'assets', f), OUT)

    cat_label = {k: l for k, l, _ in CATEGORIES}
    search_index = []
    for p in pages:
        body_html, toc = md_to_html(p['body'])
        extra = ''
        if p.get('data'):
            data = open(os.path.join(SRC, 'data', p['data']), encoding='utf-8').read()
            extra = '<script>window.PAGE_DATA = %s;</script>' % data
        toc_html = ''
        if len(toc) >= 2:
            toc_html = '<nav class="toc"><div class="toc-title">목차</div><ul>%s</ul></nav>' % ''.join(
                '<li class="toc-l%d"><a href="#%s">%s</a></li>' % (lv, hid, t) for lv, hid, t in toc)
        source = ''
        if p.get('source'):
            source = ('<p class="source">원문: <a href="%s" target="_blank" rel="noopener">%s</a> '
                      '(LUMYVERSE 공식 위키, 한국어 번역)</p>') % (p['source'], p['source'])
        crumb = cat_label.get(p.get('category'), '')
        out = render(template,
                     title=html.escape(p['title']),
                     description=html.escape(p.get('description', p['title'])),
                     sidebar=sidebar(pages, p['slug']),
                     crumb=('<div class="crumb">%s</div>' % crumb) if crumb else '',
                     content=body_html,
                     toc=toc_html,
                     source=source,
                     extra=extra,
                     bodyclass='page-' + p['slug'] + (' wide' if p.get('wide') else ''))
        open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8').write(out)
        if p['slug'] != 'index':
            search_index.append({'s': p['slug'], 't': p['title'], 'c': crumb, 'x': plain_text(p['body'])[:6000]})
    open(os.path.join(OUT, 'search-index.js'), 'w', encoding='utf-8').write(
        'window.SEARCH_INDEX=' + json.dumps(search_index, ensure_ascii=False) + ';')
    print('built %d pages -> %s' % (len(pages), OUT))


if __name__ == '__main__':
    main()
