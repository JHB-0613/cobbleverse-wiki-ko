---
title: Apex 서버 업데이트하기
category: install
order: 4
source: https://www.lumyverse.com/cobbleverse/how-to-update-apex-server/
---
> [!IMPORTANT] 월드를 백업하셨나요? **항상 백업하세요!** 무엇보다 가장 중요한 일입니다.

## 방법 1: 서버 파일 초기화 (가장 빠름)

Apex에 업데이트가 올라와 있다면 가장 빠른 방법은 **“Reset Server Files”**입니다. 이때 **“All Server Files”는 절대 선택하지 마세요.** 그래야 월드가 삭제되지 않습니다.

![Apex 패널의 Reset Server Files](up:COBBLEVERSE-APEX.png)

## 방법 2: FTP로 직접 교체

Apex 패널에서 **“FTP File Access”**를 눌러 서버에 접속한 뒤, 기존 파일을 클라이언트(런처)에 있는 최신 파일로 바꿔 주면 됩니다. 아주 간단합니다. Apex 서버에서 다음 세 폴더를 엽니다.

- **config**
- **mods**
- **datapacks**

각 폴더에 있는 기존 COBBLEVERSE 파일을 모두 삭제하고, **런처의 같은 폴더에 있는 파일**로 교체하세요.

> [!WARNING] 서버에 **이미 있던 파일만** 교체하세요. 클라이언트에만 있는 파일은 추가하지 마세요. 또한 직접 추가한 커스텀 콘텐츠가 있다면 지우지 마세요(지우면 사라집니다). 커스텀 콘텐츠는 서버가 실행되지 않을 때만 삭제하세요.

이게 전부입니다!

![FTP 업데이트 화면 1](up:COBBLEVERSE-Update-Apex.jpg)
![FTP 업데이트 화면 2](up:COBBLEVERSE-APEX-Upate.jpg)
