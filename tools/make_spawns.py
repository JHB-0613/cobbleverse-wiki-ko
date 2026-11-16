"""포켓몬 스폰 표(영문)를 한국어 JSON 데이터로 변환한다.

입력: tools/source/spawn-table-en.md (원문 표), tools/source/ko-names.csv (공식 한국어 이름)
출력: src/data/spawns.json
"""
import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 긴 표현부터 치환된다 (대소문자 무시)
PHRASES = {
    # --- 문장형 표현
    'Also by fishing in same biomes': '같은 바이옴에서 낚시로도 출현',
    'Also by fishing in same biome': '같은 바이옴에서 낚시로도 출현',
    'Also fishing in same biomes': '같은 바이옴에서 낚시로도 출현',
    'Also by fishing in': '낚시로도 출현:',
    'Also fishing in': '낚시로도 출현:',
    'Also by fishing except in': '낚시로도 출현 (제외:',
    'Also by fishing inside': '낚시로도 출현:',
    'Also by fishing': '낚시로도 출현',
    'Only Fishing in a Slime chunk': '슬라임 청크에서 낚시로만 출현',
    'Submerged or fishing': '물속 또는 낚시',
    'Seafloor or fishing': '해저 또는 낚시',
    'Hidden in Suspicious sand/gravel. Use Resurrection Machine': '수상한 모래/자갈에서 화석 획득 → 부활 장치 사용',
    'Suspicious sand/gravel. Use Resurrection Machine': '수상한 모래/자갈에서 화석 획득 → 부활 장치 사용',
    'Suspicious sand/gravel Resurrection Machine': '수상한 모래/자갈에서 화석 획득 → 부활 장치 사용',
    'Use Resurrection Machine': '부활 장치 사용',
    'Resurrection Machine': '부활 장치',
    'Suspicious sand/gravel': '수상한 모래/자갈',
    'Suspicious Sand/Gravel': '수상한 모래/자갈',
    'Can also be found wild in the': '야생에서도 발견됨:',
    'Can also be found wild in': '야생에서도 발견됨:',
    'To use the shrines you will have to first collect 8 stakes of the same type': '사당을 사용하려면 먼저 같은 종류의 말뚝 8개를 모아야 함',
    'There are 6 colored variants. Each one spawns near a flower of the same color.': '6가지 색상 변종이 있으며, 각각 같은 색의 꽃 근처에서 스폰',
    'There are 9 forms obtainable by giving 9 different dyes.': '9가지 염료를 주어 9가지 폼을 얻을 수 있음',
    'There are 20+ Forms': '20가지 이상의 폼 존재',
    'All letters available': '모든 글자 출현',
    'Bisharp must defeat 3 Bisharp in a row without ever fainting.': '절각참이 기절하지 않고 절각참 3마리를 연속으로 쓰러뜨려야 함',
    'Gimmighoul evolves when 999 Gimmighoul Coins are present in the inventory': '인벤토리에 모으령의 코인 999개가 있으면 진화',
    'Eternatus needs a Star Core to become Eternamax': '무한다이노는 스타 코어(Star Core)가 있어야 무한다이맥스가 됨',
    'Eternal Folette spawns during the night near both red flowers and blue flowers': '영원의 꽃 플라엣테는 밤에 빨간 꽃과 파란 꽃이 모두 있는 곳 근처에서 스폰',
    'Shadow Lugia (ATM x MSD ) can be obtained by crafting the Shadow Soul Stone': '섀도 루기아(ATM x MSD)는 섀도 소울 스톤(Shadow Soul Stone)을 제작해 얻을 수 있음',
    'Hero-form: Switch Palafin out (do not let it faint) Send Palafin back into battle.': '마이티폼: 돌핀맨을 교체한 뒤(기절시키지 말 것) 다시 배틀에 내보내기',
    'Midday: Evolve Rockruff during the day. Midnight: Evolve Rockruff at night. Dusk: Evolve Rockruff wolf form_dusk at Sunset (time-range: 11.000-13.000)':
        '한낮의 모습: 낮에 암멍이 진화 / 한밤중의 모습: 밤에 암멍이 진화 / 황혼의 모습: 황혼 암멍이를 해질녘(시간 11000~13000)에 진화',
    'Rockruff wolf_form=dusk spawns in a ll Mountain biomes during dusk': '황혼 암멍이(wolf_form=dusk)는 해질녘 모든 산 바이옴에서 스폰',
    'Give a Tart Apple to Applin.': '과사삭벌레에게 새콤한사과를 주기',
    'Give a Sweet Apple to Applin': '과사삭벌레에게 달콤한사과를 주기',
    'Also Obtainable by giving Vulpix a Fire Stone': '식스테일에게 불꽃의돌을 주어서도 획득 가능',
    'Evolves from Meltan when it is at level 70': '멜탄이 레벨 70일 때 진화',
    'Hisuian form spawns during the storm in the same biomes near apricorns': '히스이폼은 폭풍우 때 같은 바이옴의 규토리 근처에서 스폰',
    'Hisuian form spawns during the storm in the same biomes ear apricorns': '히스이폼은 폭풍우 때 같은 바이옴의 규토리 근처에서 스폰',
    'Needed: Scroll of Darkness or Scroll of Water': '필요: 악의 족자 또는 물의 족자',
    'Near: Redstone Block, Repeater, Redstone Torch, Daylight Detector, Comparator, Redstone Ore, Redstone Lamp, Lightining Rod, PC, Monitor, Healing Machine, Restoration Tank, Fossyl Analyzer.':
        '근처 필요: 레드스톤 블록, 레드스톤 중계기, 레드스톤 횃불, 햇빛 감지기, 레드스톤 비교기, 레드스톤 광석, 레드스톤 조명, 피뢰침, PC, 모니터, 회복 머신, 복원 탱크, 화석 분석기',
    'Core Percent Cell=10 Dripstone Caves Core Percent Cells =Lush Caves': '코어: 점적석 동굴 / 셀: 무성한 동굴',
    'Moon Phase': '달의 위상',
    'New Moon': '삭', 'Full Moon': '보름달', 'Waning Gibbous': '하현망', 'Last Quarter': '하현달', 'Waning Crescent': '그믐달',
    'Waxing Crescent': '초승달', 'First Quarter': '상현달', 'Waxing Gibbous': '상현망',
    'Low Key Form : Nature': '로우한 모습: 성격', 'Amped Form : Nature': '하이한 모습: 성격',
    'Lonely': '외로움', 'Bold': '대담', 'Relaxed': '무사태평', 'Timid': '겁쟁이', 'Serious': '성실', 'Modest': '조심',
    'Mild': '의젓', 'Quiet': '냉정', 'Bashful': '수줍음', 'Calm': '차분', 'Gentle': '얌전', 'Careful': '신중',
    'Hardy': '노력', 'Brave': '용감', 'Adamant': '고집', 'Naughty': '개구쟁이', 'Docile': '온순', 'Impish': '장난꾸러기',
    'Lax': '촐랑', 'Hasty': '성급', 'Jolly': '명랑', 'Naive': '천진난만', 'Rash': '덜렁', 'Sassy': '건방', 'Quirky': '변덕',
    'Baile Style': '이글이글스타일', 'Pom-Pom Style': '파칙파칙스타일', 'Pa’u Style': '훌라훌라스타일', 'Sensu Style': '하늘하늘스타일',
    'Heart Form : fishing in Mushroom Island': '하트 모양: 버섯 섬에서 낚시',
    'Red Mooshtank spawns ins': '빨간 무쉬탱크 스폰:',
    'Bloodmoon form spawns in': '붉은달 폼 스폰:',
    'Origin Forme': '오리진폼',
    'Normal: All Overworld biome': '노말: 모든 오버월드 바이옴',
    'Need Fossilized Bird and Fossilized Drake': '필요: 화석새 + 화석용', 'Need Fossilized Bird and Fossilized Dino': '필요: 화석새 + 화석공룡',
    'Need Fossilized Drake and Fossilized Fish': '필요: 화석용 + 화석물고기', 'Need Fossilized Dino and Fossilized Fish': '필요: 화석공룡 + 화석물고기',
    'Need Pebble Relic': '필요: 페블 렐릭(Pebble Relic)', 'Need Cryo Relic': '필요: 크라이오 렐릭(Cryo Relic)',
    'Need Metal Relic': '필요: 메탈 렐릭(Metal Relic)', 'Need Spark Relic': '필요: 스파크 렐릭(Spark Relic)',
    'Need Draco Relic': '필요: 드라코 렐릭(Draco Relic)', 'Need Ruby Dew': '필요: 루비 이슬(Ruby Dew)',
    'Need Sapphire Dew': '필요: 사파이어 이슬(Sapphire Dew)', 'Need Ocean Core': '필요: 오션 코어(Ocean Core)',
    'Need Earth Core': '필요: 어스 코어(Earth Core)', 'Need Sky Core': '필요: 스카이 코어(Sky Core)',
    'Need Melodic Tape (Vol. 1)': '필요: 멜로딕 테이프 Vol.1(Melodic Tape)', 'Need Meteorite Crystal': '필요: 운석 결정(Meteorite Crystal)',
    'Need Iceroot carrots': '필요: 얼음뿌리당근(Iceroot Carrot)', 'Need Shaderoot carrot': '필요: 그늘뿌리당근(Shaderoot Carrot)',
    'Need Calyrex Crown': '필요: 버드렉스 왕관(Calyrex Crown)',
    'Zygarde Core/cells': '지가르데 코어/셀',
    # --- 폼 / 지역
    'Alolan Region bias spawns in': '알로라폼 스폰:', 'Galarian Region bias spawns in': '가라르폼 스폰:',
    'Hisuian region bias spawns in': '히스이폼 스폰:', 'Hisuian region bias spawn in': '히스이폼 스폰:',
    'Alolan form is Uncommon and spawns in': '알로라폼은 드묾 등급이며 스폰:',
    'Alolan form spawns in': '알로라폼 스폰:', 'Alolan Form spawns in': '알로라폼 스폰:',
    'Galarian form spawns in': '가라르폼 스폰:', 'Galarian Form spawns in': '가라르폼 스폰:', 'Galarian from spawns in': '가라르폼 스폰:',
    'Galarian form spawns under Dyna Tree': '가라르폼은 다이나 트리 아래에서 스폰',
    'Hisuian form spawns ins': '히스이폼 스폰:', 'Hisuian form spawns in': '히스이폼 스폰:', 'Hisuian form spawn in': '히스이폼 스폰:',
    'Paldean forms spawns in': '팔데아폼 스폰:', 'Paldean form spawns ins': '팔데아폼 스폰:', 'Paldean form spawns in': '팔데아폼 스폰:',
    'Valencian forms spoawns in': '발렌시아폼 스폰:', 'Valencian form spawns': '발렌시아폼 스폰', 'Valencian form': '발렌시아폼',
    'Counterfeit Form': '가짜폼', 'Artisan Form': '범작폼', 'Unremarkable Form': '범작폼', 'Masterpiece Form': '걸작폼',
    'Antique Form': '진품폼', 'Phony Form': '가짜폼', 'Sandy-Form': '모래땅도롱치마', 'Trash-Form': '슈레도롱치마', 'Plant- Form': '초목도롱치마',
    'East Form': '동쪽바다', 'West Form': '서쪽바다', 'White form': '흰색', 'Blue Form': '파란색', 'Red form': '빨간색',
    'Forms': '폼', 'Apricot': '살구색', 'Purple': '보라색', 'Calico': '얼룩무늬', 'Brown': '갈색', 'Gray': '회색',
    'Cosplay Belle': '마담 코스프레', 'Cosplay Libre': '마스크드 코스프레', 'Cosplay Phd': '닥터 코스프레',
    'Cosplay Pop Star': '아이돌 코스프레', 'Cosplay Rock Star': '하드록 코스프레',
    'Blue, Red, White, Yellow, Pink, Orange': '파랑, 빨강, 하양, 노랑, 분홍, 주황',
    'Red :': '빨강:', 'Orange :': '주황:', 'Yellow :': '노랑:', 'Green :': '초록:', 'Blue :': '파랑:', 'Violet :': '보라:', 'Indigo :': '남색:', 'Pink :': '분홍:',
    'Forecast Sunny': '포캐스트 태양', 'Forecast Snowy': '포캐스트 설운', 'Forecast': '포캐스트',
    # --- 구조물
    'Structures': '구조물', 'Structure': '구조물', 'Stucture': '구조물',
    'Ocean Ruins': '해저 폐허', 'Ancient City': '고대 도시', 'Desert Pyramid': '사막 피라미드', 'Jungle Pyramid': '정글 피라미드',
    'Jungle Temple': '정글 사원', 'Jungle pyramid': '정글 피라미드', 'trial ruins': '시련 폐허', 'ruins': '폐허',
    'Mansion Structures': '삼림 대저택', 'Mansion structure': '삼림 대저택', 'Mansion': '삼림 대저택', 'End City': '엔드 시티',
    'Swamp hut': '늪 오두막', 'Illager Outpost': '약탈자 전초기지', 'Ruined Portal (Overworld)': '폐허가 된 차원문(오버월드)',
    'Cobblemon Ruin Structures': '코블몬 폐허 구조물', 'Cobblemon ruins': '코블몬 폐허', 'Cobblemon Ruins': '코블몬 폐허', 'Cobblemon Ruin': '코블몬 폐허',
    'Gimmighoul Towers': '모으령 타워', 'minecraft villages': '마인크래프트 마을', 'Minecraft villages': '마인크래프트 마을',
    'Minecraft Village': '마인크래프트 마을', 'minecraft village': '마인크래프트 마을', 'Villages': '마을', 'villages': '마을',
    'minecraft igloo': '마인크래프트 이글루', 'Amethyst geode': '자수정 정동', 'Amethyst Geode': '자수정 정동',
    'Burned Tower': '불탄탑(Burned Tower)', 'Bell Tower': '방울탑(Bell Tower)', 'Whirl Island': '소용돌이섬(Whirl Island)',
    'Ilex Shrine': '너도밤나무숲 사당(Ilex Shrine)', 'ArticunoTower': '프리져 타워', 'Articuno Tower': '프리져 타워',
    'Zapdos Tower': '썬더 타워', 'Moltres Tower': '파이어 타워', 'Team Rocket Tower': '로켓단 타워', 'Origin Temple': '기원의 신전(Origin Temple)',
    'Regirock temple': '레지락 신전', 'Regice temple': '레지아이스 신전', 'Registeel temple': '레지스틸 신전',
    'Secret Garden': '비밀의 정원(Secret Garden)', 'Submerged in its Temple': '신전 안 물속', 'Volcano': '화산',
    'Sky Pillar': '하늘기둥(Sky Pillar)', 'Wish Cave': '소원 동굴(Wish Cave)', 'Deoxys Meteorite': '테오키스 운석',
    'Lake Acuity': '예지호수(Lake Acuity)', 'Lake Verity': '진실호수(Lake Verity)', 'Lake Valor': '입지호수(Lake Valor)',
    'Stark Mountain': '전경산(Stark Mountain)', 'Snowpoint Temple': '선단 신전(Snowpoint Temple)', 'Giratina Island': '기라티나 섬',
    'FullMoon Island': '만월섬(Fullmoon Island)', 'Newmoon Island': '신월섬(Newmoon Island)', 'Flower Paradise': '꽃의 낙원(Flower Paradise)',
    'Sinnoh Temple': '신오 신전', 'Spear Pillar': '창기둥(Spear Pillar)', 'Split Decision Temple': '갈림길 신전(Split Decision Temple)',
    'Crown Cemetery Spire': '왕관 묘지/첨탑', 'Crown Cemetery': '왕관 묘지(Crown Cemetery)', 'Crown Spire': '왕관 첨탑(Crown Spire)',
    'Dawn Tower': '새벽 타워', 'Dusk Tower': '황혼 타워', 'Dyna Tree': '다이나 트리', 'Stonjourner Henge Ruins': '돌헨진 환상열석 폐허',
    'Grasswither Shrine': '초목 사당(Grasswither Shrine)', 'Icerend Shrine': '빙결 사당(Icerend Shrine)',
    'Groundblight Shrine': '대지 사당(Groundblight Shrine)', 'Firescourge Shrine': '화염 사당(Firescourge Shrine)',
    'Legendary Monuments': '레전더리 모뉴먼트', 'Mushroom Island': '버섯 섬',
    # --- 바이옴 (마인크래프트 공식 한국어 명칭 기준)
    'All Overworld biomes except': '모든 오버월드 바이옴 (제외:', 'Overworld biomes except': '오버월드 바이옴 (제외:',
    'All Forest biomes except': '모든 숲 바이옴 (제외:', 'All River biomes except': '모든 강 바이옴 (제외:',
    'All Ocean biomes except': '모든 바다 바이옴 (제외:', 'River biomes except': '강 바이옴 (제외:', 'Caves except': '동굴 (제외:',
    'All Overworld biomes': '모든 오버월드 바이옴', 'All Overworld biome': '모든 오버월드 바이옴', 'Overworld biomes': '오버월드 바이옴',
    'Overworld Underground': '오버월드 지하', 'All Ocean Biomes': '모든 바다 바이옴', 'All Ocean biomes': '모든 바다 바이옴', 'all Ocean Biomes': '모든 바다 바이옴',
    'All Forest biomes': '모든 숲 바이옴', 'Forest biomes': '숲 바이옴', 'All Forests': '모든 숲', 'Forests': '숲',
    'All Jungle Biomes': '모든 정글 바이옴', 'All Jungle biomes': '모든 정글 바이옴', 'All Taiga biomes': '모든 타이가 바이옴',
    'All Plains biomes': '모든 평원 바이옴', 'All Hills biomes': '모든 언덕 바이옴', 'Hills biomes': '언덕 바이옴',
    'All River biomes': '모든 강 바이옴', 'All Savanna biomes': '모든 사바나 바이옴', 'All Nether Biomes': '모든 네더 바이옴',
    'All Nether biomes': '모든 네더 바이옴', 'All End biomes': '모든 엔드 바이옴', 'All Mountain biomes': '모든 산 바이옴',
    'All Cold biomes': '모든 추운 바이옴', 'Desert biomes': '사막 바이옴', 'Taiga biomes': '타이가 바이옴',
    'Old Growth Pine/Spruce Taiga': '소나무/가문비나무 원시 타이가', 'Old Growth Birch Forest': '자작나무 원시림', 'Old Growth Birch Fores': '자작나무 원시림',
    'Old Growth Pine Taiga': '소나무 원시 타이가', 'Old Growth Spruce Taiga': '가문비나무 원시 타이가', 'Old Growth Taiga': '원시 타이가',
    'Windswept Gravelly Hills': '흩날리는 자갈 언덕', 'Windswept gravelly Hills': '흩날리는 자갈 언덕', 'Windswept Gravelly hills': '흩날리는 자갈 언덕',
    'Windswept Savanna': '흩날리는 사바나', 'Windswept Forests': '흩날리는 숲', 'Windswept Forest': '흩날리는 숲',
    'Windswept Hills': '흩날리는 언덕', 'Windswep Hills': '흩날리는 언덕',
    'Deep Lukewarm Ocean': '깊은 미지근한 바다', 'Deep Frozen Ocean': '깊은 얼어붙은 바다', 'Deep Cold Ocean': '깊은 차가운 바다',
    'Deep Warm Ocean': '깊은 따뜻한 바다', 'Deep Ocean': '깊은 바다', 'Lukewarm Ocean': '미지근한 바다', 'Frozen Ocean': '얼어붙은 바다',
    'Cold Ocean': '차가운 바다', 'Coild Ocean': '차가운 바다', 'Warm Ocean': '따뜻한 바다', 'Oceam': '바다', 'Ocean': '바다',
    'Sunflower Plains': '해바라기 평원', 'Sunflwoer Plains': '해바라기 평원', 'Sunflower Forest': '해바라기 숲', 'Snowy Plains': '눈 덮인 평원',
    'Plasins': '평원', 'Plains': '평원', 'plains': '평원', 'Plain': '평원',
    'Flower Forest': '꽃 숲', 'Birch Forest': '자작나무 숲', 'Dark Oak Forest': '짙은 참나무 숲', 'Dark Oak Fores': '짙은 참나무 숲',
    'Dark Forest Hills': '어두운 숲 언덕', 'Dark Forest': '어두운 숲', 'dark Forest': '어두운 숲', 'Oak Forest': '참나무 숲',
    'Bamboo Forest': '대나무 숲', 'Snow Forest': '눈 덮인 숲', 'Lavender Forest': '라벤더 숲',
    'Bamboo Jungle': '대나무 정글', 'Sparse Junglea': '드문드문한 정글', 'Sparse Jungle': '드문드문한 정글', 'Jungle': '정글', 'ungle': '정글',
    'Snowy Taiga': '눈 덮인 타이가', 'Taiga': '타이가', 'aiga': '타이가',
    'Mangrove Swamp': '맹그로브 늪', 'Mangroove Swamp': '맹그로브 늪', 'Swamp': '늪',
    'Savanna Plateau': '사바나 고원', 'Savannah': '사바나', 'Savanna': '사바나', 'Svanna': '사바나',
    'Eroded Badlands': '침식된 악지', 'eroded Badlands': '침식된 악지', 'Eroded Badland': '침식된 악지', 'Wooded Badlands': '나무가 우거진 악지',
    'Snowy Badlands': '눈 덮인 악지(Snowy Badlands)', 'Badlands': '악지',
    'Cherry Grove': '벚나무 숲', 'Snowy Grove': '눈 덮인 수림', 'Grove': '수림',
    'Snowy Slopes': '눈 덮인 비탈', 'S nowy Slopes': '눈 덮인 비탈', 'Snowy SLopes': '눈 덮인 비탈', 'Snowy Slope': '눈 덮인 비탈',
    'Stony Slopes': '바위 비탈', 'Frozen Peaks': '얼어붙은 봉우리', 'Jagged Peaks': '뾰족한 봉우리', 'Stony Peaks': '바위 봉우리',
    'S tony Peaks': '바위 봉우리', 'Stony Peak': '바위 봉우리', 'Stony Shore': '돌 해안', 'Snowy Beach': '눈 덮인 해변', 'Beach': '해변', 'beach': '해변',
    'Frozen River': '얼어붙은 강', 'Frozen Rive': '얼어붙은 강', 'River': '강', 'Ice Spikes': '역고드름', 'Frozen Spike': '역고드름',
    'Meadowomes': '목초지', 'MeadowPlains': '목초지, 평원', 'Meadow': '목초지',
    'Mushroom Fields': '버섯 들판', 'Dripstone Caves': '점적석 동굴', 'Drpstone Cave': '점적석 동굴', 'Lush Caves': '무성한 동굴', 'Lush Cave': '무성한 동굴',
    'Deep Dark': '깊은 어둠', 'Fungal Caves': '균류 동굴', 'Undeground Jungle': '지하 정글', 'Caves': '동굴', 'Cave': '동굴', 'Desert': '사막', 'desert': '사막',
    'Nether Wastes': '네더 황무지', 'Soul Sand Valley': '영혼 모래 골짜기', 'Crimson Forest': '진홍빛 숲', 'Warped Forest': '뒤틀린 숲',
    'Basalt Deltas': '현무암 삼각주', 'The End': '디 엔드', 'End Highlands': '엔드 고원', 'Small End Islands': '작은 엔드 섬',
    # 테라리스 등 커스텀 바이옴 (원어 병기)
    'Blooming Plateau': '꽃피는 고원(Blooming Plateau)', 'Blooming Valley': '꽃피는 골짜기(Blooming Valley)',
    'Arid Highlands': '건조한 고지대(Arid Highlands)', 'Alphine Highlands': '알파인 고지대(Alpine Highlands)',
    'Glacial Chasm': '빙하 협곡(Glacial Chasm)', 'Lush Desert': '무성한 사막(Lush Desert)', 'Wintry Lowlands': '겨울 저지대(Wintry Lowlands)',
    'Cold Shurbland': '차가운 관목지(Cold Shrubland)', 'Sakura Grove': '사쿠라 수림(Sakura Grove)', 'Sakura Valley': '사쿠라 골짜기(Sakura Valley)',
    'Lavender Valley': '라벤더 골짜기(Lavender Valley)', 'Moonlight Valley': '달빛 골짜기(Moonlight Valley)', 'Moonlight': '달빛',
    'Frozen Cliffss': '얼어붙은 절벽(Frozen Cliffs)', 'Frozen Cliffs': '얼어붙은 절벽(Frozen Cliffs)', 'White Cliffs': '하얀 절벽(White Cliffs)',
    'Steppe': '스텝(Steppe)', 'Frostfire Caves': '서리불 동굴(Frostfire Caves)', 'Dripstone Oasis': '점적석 오아시스',
    'Distorted Dimension': '깨어진 세계 차원', 'Nightmare Dimension': '악몽 차원', 'Origin Dimension': '기원 차원',
    # 화석 사이트 등
    'Fossil': '화석', 'Preserved Skeleton': '보존된 골격', 'Powdered Deposit': '가루 퇴적층', 'Sunscorched Den': '그을린 굴',
    'Sunscorched Remains': '그을린 유해', 'Lush Den': '무성한 굴', 'Sandy Den': '모래 굴', 'Oak Tree': '참나무', 'Spruce Tree': '가문비나무',
    'Birch Tree': '자작나무', 'Mossy Pond': '이끼 연못', 'Frozen Pond': '얼어붙은 연못', 'Mud Pit': '진흙 구덩이',
    'Vibrant Hydrothermal Vents': '생동하는 열수구', 'Hydrothermal Vents': '열수구', 'Rooted Pit': '뿌리 구덩이', 'Suspicious Mound': '수상한 둔덕',
    'Suspicious mound': '수상한 둔덕', 'Submerged Impact': '수몰된 충돌구', 'Submerged Spike': '수몰된 가시', 'Underwater Fissure': '수중 균열',
    'Eroded Pillar': '침식된 기둥', 'Enhydro Agate': '엔하이드로 마노', 'Seagrass': '해초',
    'Loot dropped by the Team Rocket Scientist': '로켓단 과학자의 전리품 드롭',
    'Nether Star': '네더의 별', 'Dubious Disk': '괴상한패치', 'Doom Fossil': '둠 화석',
    'Evolution from': '진화:', 'Evolves from': '진화:',
    # --- 조건
    'During the Night, in': '밤, 장소:', 'During a Thunderstorm': '뇌우 중', 'During a storm': '폭풍우 중', 'During the Rain': '비 오는 중',
    'during the storm': '폭풍우 중', 'during a thunderstorm': '뇌우 중', 'during a Storm': '폭풍우 중', 'during the night': '밤',
    'during the day': '낮', 'during dusk': '해질녘', 'Near lightining rod, during a storm': '폭풍우 중 피뢰침 근처',
    'More common during thunderstorm': '뇌우 때 더 자주 출현', 'More common in the daytime': '낮에 더 자주 출현',
    'More common during rain': '비 올 때 더 자주 출현', 'More common near a coweb with Night and weather clear': '밤·맑은 날씨에 거미줄 근처에서 더 자주 출현',
    'More common inside': '다음 장소에서 더 자주 출현:', 'more common inside': '다음 장소에서 더 자주 출현:',
    'More common near beehives': '벌집 근처에서 더 자주 출현', 'More common near': '다음 근처에서 더 자주 출현:', 'more common near': '다음 근처에서 더 자주 출현:',
    'More common in': '다음 장소에서 더 자주 출현:', 'more common in': '다음 장소에서 더 자주 출현:', 'Common in': '자주 출현:',
    'Only in': '다음 장소에서만:', 'Also in': '다음 장소에서도:', 'only in': '다음 장소에서만:',
    'Near a Minecraft Village': '마인크래프트 마을 근처', 'Near a Pumpkin or Carved Pumpkin': '호박 또는 조각된 호박 근처',
    'Near White Bed': '흰색 침대 근처', 'Near Medicinal Leek': '약용 대파 근처', 'Near Coal Ore': '석탄 광석 근처',
    'Near Diamond Ore': '다이아몬드 광석 근처', 'Near a Purpur block': '퍼퍼 블록 근처', 'Near Iron Block': '철 블록 근처',
    'Near Cobblemon Berries': '코블몬 나무열매 근처', 'Near Lava': '용암 근처', 'Near a PC': 'PC 근처', 'Near a cake': '케이크 근처',
    'near Lava or Water': '용암 또는 물 근처', 'near iron ores': '철 광석 근처', 'near a dead coral': '죽은 산호 근처', 'near Kelp Plant': '켈프 근처',
    'near a': '근처:', 'Near': '근처',
    'Time-range: morning': '시간대: 아침', 'Weather Clear': '맑은 날씨', 'Weather clear': '맑은 날씨', 'weather clear': '맑은 날씨',
    'Thunderstorm': '뇌우', 'Storm': '폭풍우', 'Raining': '비', 'Rain': '비', 'Day/Night': '낮/밤', 'Nigh,': '밤,',
    'Night': '밤', 'Day': '낮', 'Dusk': '해질녘', 'Midnight': '한밤중',
    'Overworld': '오버월드', 'biomes': '바이옴', 'Biomes': '바이옴', 'biome': '바이옴',
    'except': '제외', 'Also': '또한', 'holding an anvil': '모루를 든 상태', 'in Caves': '동굴', 'in': '',
    'Hisuian': '히스이', 'Galarian': '가라르', 'Alolan': '알로라', 'Paldean': '팔데아',
    'Max Y': '최대 Y', 'Min Y': '최소 Y', 'MaxY': '최대 Y', 'MinY': '최소 Y',
}

RARITY = {
    'common': ('흔함', ['common']), 'uncommon': ('드묾', ['uncommon']), 'rare': ('희귀', ['rare']),
    'ultra-rare': ('초희귀', ['ultra']), 'uncommon/rare': ('드묾/희귀', ['uncommon', 'rare']),
    'common/uncommon': ('흔함/드묾', ['common', 'uncommon']), 'common/rare': ('흔함/희귀', ['common', 'rare']),
}

GEN = {
    'KANTO': '1세대 · 관동', 'JOHTO': '2세대 · 성도', 'HOENN': '3세대 · 호연', 'SINNOH': '4세대 · 신오',
    'UNOVA': '5세대 · 하나', 'KALOS': '6세대 · 칼로스', 'ALOLA': '7세대 · 알로라', 'GALAR': '8세대 · 가라르', 'PALDEA': '9세대 · 팔데아',
}


def build_translator(names_en_to_ko):
    table = {}
    for k, v in PHRASES.items():
        table.setdefault(k.lower(), v)
    for en, ko in names_en_to_ko.items():
        table.setdefault(en.lower(), ko)
    table.update({"’s evolution": ' 진화', "'s evolution": ' 진화', 'ultra-rare': '초희귀', 'or': '또는', 'and': '및',
                  'type: null': '타입:널', 'type null': '타입:널', 'forest': '숲', 'spawns': '스폰', 'with': '', 'sky light': '하늘 빛 밝기', 'can also be found wild': '야생에서도 발견됨', 'during': '', 'the': ''})
    keys = sorted(table, key=len, reverse=True)
    pattern = re.compile('|'.join(
        (r'(?<![A-Za-z])' if k[0].isalpha() else '') + re.escape(k) + (r'(?![A-Za-z])' if k[-1].isalpha() else '')
        for k in keys), re.I)

    def tr(text):
        text = text.replace('\xa0', ' ').replace('��', '’')
        if not text:
            return ''
        text = re.sub(r'\s+', ' ', text)
        out = pattern.sub(lambda m: table[m.group(0).lower()], text)
        out = re.sub(r'\s+', ' ', out).strip(' ,')
        # "(제외: X" 형태의 괄호 닫기
        if out.count('(') > out.count(')'):
            out += ')'
        return out.replace(' ,', ',').replace('( ', '(')

    return tr


def main():
    names = {}
    en_to_ko = {}
    for row in csv.DictReader(open(os.path.join(HERE, 'source', 'ko-names.csv'), encoding='utf-8')):
        names[int(row['id'])] = row['ko']
        if row['en']:
            en_to_ko[row['en']] = row['ko']
    tr = build_translator(en_to_ko)

    data, gen = [], ''
    for line in open(os.path.join(HERE, 'source', 'spawn-table-en.md'), encoding='utf-8'):
        m = re.match(r'^## GEN\. \d+ – (\w+)', line)
        if m:
            gen = GEN.get(m.group(1), m.group(1))
            continue
        if not line.startswith('| #'):
            continue
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        num = int(re.sub(r'\D', '', c[0]) or 0)
        rar = RARITY.get(c[4].lower(), (c[4], []))
        model = c[2].replace('Showdonw', 'Showdown')
        data.append({
            'n': '#%04d' % num, 'g': gen, 'ko': names.get(num, c[1]), 'en': c[1], 'm': model,
            'r': rar[0], 'rk': rar[1],
            's': tr(c[3]), 'c': tr(c[5]), 'f': tr(c[6]),
            'os': c[3], 'oc': c[5], 'of': c[6],
        })
    os.makedirs(os.path.join(ROOT, 'src', 'data'), exist_ok=True)
    json.dump(data, open(os.path.join(ROOT, 'src', 'data', 'spawns.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, separators=(',', ':'))
    print('%d entries' % len(data))


if __name__ == '__main__':
    main()
