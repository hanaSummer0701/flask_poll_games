#!/bin/bash
# Flask 프로젝트 폴더로 이동
cd /home/ubuntu/flask_poll_games

# 가상 환경 활성화
source bin/activate

# Flask 앱을 백그라운드에서 실행
nohup python3 app.py &
