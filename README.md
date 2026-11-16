# COBBLEVERSE 한국어 위키

[LUMYVERSE COBBLEVERSE Wiki](https://www.lumyverse.com/cobbleverse/)의 전체 문서(47페이지)를 한국어로 옮긴 정적 위키 사이트입니다.

## 보기

`site/index.html`을 브라우저로 열면 됩니다 (서버 불필요). 로컬 서버로 보려면:

```bash
python -m http.server 8765 --directory site
```

## 구조

| 경로 | 내용 |
|---|---|
| `src/pages/*.md` | 한국어 원고 (마크다운 + 머리말 `title`, `category`, `order`, `source`) |
| `src/template.html`, `src/assets/` | 페이지 틀, CSS, 검색·스폰 목록 스크립트 |
| `src/data/spawns.json` | 포켓몬 1,025마리 스폰 데이터 (자동 생성) |
| `tools/make_spawns.py` | 원문 스폰 표 → 한국어 JSON 변환 (바이옴·조건 사전 포함) |
| `tools/ko_pokemon.py` | 원고 속 영문 포켓몬 이름을 공식 한국어 이름으로 변환 (조사 자동 보정) |
| `tools/source/` | 원문 스폰 표, 공식 한국어 포켓몬 이름 목록 (PokeAPI) |
| `build.py` | `src/` → `site/` 빌드 |

## 수정 후 다시 빌드

```bash
python build.py
```

스폰 번역 사전을 고쳤다면 먼저 `python tools/make_spawns.py`를 실행하세요.

원고 문법: `> [!TIP]` / `> [!WARNING]` / `> [!IMPORTANT]` / `> [!NOTE]` 콜아웃, `![설명](up:파일명)`은 원본 위키 업로드 이미지 단축 표기, 연속된 이미지 줄은 갤러리로 묶입니다.
