"""원고 파일 속 영문 포켓몬 이름을 공식 한국어 이름으로 바꾼다.

사용법: python tools/ko_pokemon.py src/pages/파일.md [...]
- 링크/이미지/코드(`...`) 안은 건드리지 않는다.
- Mega / Hisuian / Galarian / Alolan / Shiny 접두어도 함께 번역한다.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
names = {}
for row in csv.DictReader(open(os.path.join(HERE, 'source', 'ko-names.csv'), encoding='utf-8')):
    if row['en']:
        names[row['en']] = row['ko']
        names[row['en'].replace('’', "'")] = row['ko']
names.update({'Farfetch’d': '파오리', 'Zygarde Core': '지가르데 코어', 'Zygarde 50%': '지가르데 50%폼'})
PREFIX = {'Mega': '메가', 'Hisuian': '히스이', 'Galarian': '가라르', 'Alolan': '알로라', 'Shiny': '이로치'}
# 일반 영어 단어와 겹치는 이름은 제외
SKIP = {'Unown', 'Ditto'}

keys = sorted((k for k in names if k not in SKIP), key=len, reverse=True)
name_re = '|'.join(re.escape(k) for k in keys)
pat = re.compile(r'(?<![A-Za-z0-9/(\[.-])(?:(Mega|Hisuian|Galarian|Alolan|Shiny) )?(' + name_re + r')(?![A-Za-z0-9-])')
protect = re.compile(r'(`[^`]*`|!\[[^\]]*\]\([^)]*\)|\]\([^)]*\)|https?://\S+)')


PAIRS = {'와': ('과', '와'), '과': ('과', '와'), '을': ('을', '를'), '를': ('을', '를'),
         '이': ('이', '가'), '가': ('이', '가'), '은': ('은', '는'), '는': ('은', '는')}
ko_re = '|'.join(re.escape(v) for v in sorted(set(names.values()), key=len, reverse=True))
particle_pat = re.compile('(' + ko_re + ')([와과을를이가은는])(?=[\\s,.!?)]|$)')


def has_batchim(word):
    ch = word[-1]
    return '가' <= ch <= '힣' and (ord(ch) - 0xAC00) % 28 != 0


def fix_particles(text):
    def sub(m):
        word, p = m.group(1), m.group(2)
        with_b, without_b = PAIRS[p]
        return word + (with_b if has_batchim(word) else without_b)
    return particle_pat.sub(sub, text)


def convert(text):
    def sub(m):
        pre = PREFIX[m.group(1)] + ' ' if m.group(1) else ''
        return pre + names[m.group(2)]
    parts = protect.split(text)
    return fix_particles(''.join(p if i % 2 else pat.sub(sub, p) for i, p in enumerate(parts)))


for path in sys.argv[1:]:
    raw = open(path, encoding='utf-8').read()
    head, sep, body = raw.partition('\n---\n')
    out = head + sep + convert(body)
    open(path, 'w', encoding='utf-8').write(out)
    print('converted', path)
