---
title: 마인크래프트 로그 공유하는 법
category: settings
order: 1
source: https://www.lumyverse.com/cobbleverse/how-to-share-your-minecraft-logs/
---
COBBLEVERSE에서 크래시가 발생하면, 먼저 **아무것도 수정하지 않은 상태**로 모드팩을 사용하고 있는지 확인하세요. 추가 모드, 데이터팩, 리소스팩이 없어야 합니다. 가장 흔한 크래시 원인은 모드팩과 호환되지 않는 모드를 추가한 경우입니다. 너무 걱정하기 전에 먼저 그것들을 제거하고, **항상 월드를 백업**하세요.

수정 없이 모드팩을 사용 중인데도 문제가 생긴다면, 원인을 파악하기 위해 **로그 파일**과 **사용 중인 런처 이름**이 필요합니다. 플랫폼별로 올바르게 업로드하는 방법은 다음과 같습니다.

## 1. Modrinth

Modrinth 앱은 내장 기능 덕분에 아주 간단합니다.

1. 런처 사이드 메뉴의 **“Logs”** 섹션에서 **“Share”** 버튼을 클릭합니다.
2. 런처가 로그를 자동으로 업로드하고 **고유 링크**를 생성합니다.
3. 링크를 복사해 전용 [Discord 서버](https://discord.lumy.fun)의 알맞은 채널에 보내세요.

![Modrinth 로그 공유](up:image-35.png)
![latest 로그](up:COBBLEVERSE-Latest-log-1-1024x371.jpg)

## 2. CurseForge

CurseForge에는 아직 직접 공유 버튼이 없으므로, 파일을 직접 찾아 [mclo.gs](https://mclo.gs/) 같은 외부 서비스를 이용해야 합니다.

1. CurseForge 앱을 열고 **모드팩 로고를 우클릭**합니다.
2. **“Open Folder”**를 선택합니다.
3. 열린 폴더에서 **logs** 하위 폴더로 들어갑니다.
4. **latest** 파일을 찾습니다.
5. latest 파일을 텍스트 편집기(메모장 등)로 열어 **내용 전체를 복사**한 뒤 [mclo.gs](https://mclo.gs/)에 붙여넣습니다.
6. 또는 latest 파일을 mclogs 웹페이지로 **드래그 앤 드롭**해도 됩니다.
7. **“Save”**를 누르고 생성된 URL을 복사해 Discord의 해당 지원 채널에 보내세요.

![Open Folder](up:image-40.png)
![logs 폴더](up:image-37.png)
![mclo.gs](up:image-39.png)

## 3. 서버 로그

서버에서 모드팩을 운영 중이라면 **서버 로그**도 필요할 수 있습니다. 서버 제어판이나 FTP로 접근할 수 있습니다.

1. 서버의 콘솔 또는 파일 관리자를 엽니다.
2. **logs** 폴더를 찾습니다.
3. 안에서 **latest** 파일을 찾습니다.
4. CurseForge와 똑같이 파일을 열어 **내용 전체를 복사**하고 [mclo.gs](https://mclo.gs/)에 붙여넣습니다.
