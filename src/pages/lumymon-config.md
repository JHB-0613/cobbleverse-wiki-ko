---
title: LumyMon 설정 변경하기
category: tutorials
order: 7
source: https://www.lumyverse.com/cobbleverse/how-to-change-lumymon-config/
---
**LumyMon**은 몇 가지 새로운 기능을 추가합니다. 이 기능들은 config 폴더의 설정 파일을 열어 아주 간단하게 바꿀 수 있습니다.

1. CurseForge나 Modrinth에서 **모드팩 로고를 우클릭**합니다.
2. **“Open folder”**를 선택합니다.
3. **config** 폴더를 찾아 **lumymon.json** 파일을 엽니다.

![모드팩 폴더 열기](up:image-44-1024x292.png)
![config 폴더](up:image-46.png)
![lumymon.json](up:image-45.png)

## 설정 항목 설명

JSON 파일을 열면 다음 항목이 있습니다. 하나씩 살펴보겠습니다.

| 설정 | 설명 |
|---|---|
| `remotePcEnabled` | `true`이면 **P 키**를 눌러 어디서든 PC에 접속할 수 있습니다. `false`이면 실제 PC를 제작해야 합니다. |
| `paleGardenResinGeneration` | `true`이면 **창백한 정원(Pale Garden)** 바이옴에서 수지(Resin)가 자동 생성됩니다. COBBLEVERSE에는 수지를 떨어뜨리는 크리킹이 없으므로 필수 기능입니다. |
| `creakingToTrevenant` | `true`이면 크리킹 대신 **대로트(Trevenant)**가 스폰됩니다. |
| `ghastToGastly` | `true`이면 말라붙은 가스트(Dried Ghast)가 해피 가스트 대신 **고오스**로 변합니다. |
| `enablePokeSnackBlacklist` | `true`이면 목록에 있는 포켓몬에게 **포케스낵(PokeSnack)**이 작동하지 않습니다. 제한을 없애고 모든 포켓몬에게 포케스낵이 작동하게 하려면 `false`로 설정하세요. |
| `giveCheersOnRaidStart` | (0.6.5+) 레이드 입장 시 응원 아이템 자동 지급 여부 |
| `raidCheerCount` | (0.6.5+) 플레이어가 받을 응원 아이템 종류별 개수 (기본값 3) |
| `blacklistedPokeSnackSpawns` | 포케스낵 블랙리스트로 사용할 목록 파일 이름들 |

![설정 파일 내용](up:image-47.png)

## LumyMon 포케스낵 블랙리스트 살펴보기

LumyMon 모드 안의 기존 포켓몬 목록을 보려면 다음 단계를 따르세요.

1. config 폴더를 찾았던 처음 폴더로 돌아갑니다 (런처의 “Open folder”).
2. 이번에는 **mods** 폴더를 엽니다.
3. 모드 파일은 **.jar** 형식이며 압축 폴더처럼 동작합니다. 제대로 열려면 **7-Zip**이나 **WinRAR**가 설치되어 있어야 합니다.
4. 파일을 열면 **data** 폴더가 보입니다. data 폴더는 게임의 모든 규칙이 저장된 모드의 ‘두뇌’라고 생각하면 됩니다.
5. 포켓몬 목록을 찾으려면 **data › lumymon › poke_snack_blacklist** 순서로 폴더를 엽니다.

이 폴더 안에는 **5개의 목록**(`custom`, `legendary`, `mythical`, `paradox`, `ultrabeast`)이 있습니다. 이 목록 이름을 설정 파일에 추가해 해당 포켓몬이 스폰되지 않게 하거나, 직접 목록을 만들어 데이터팩 안의 **똑같은 경로**(`data/lumymon/poke_snack_blacklist/파일이름.json`)에 넣을 수도 있습니다.
