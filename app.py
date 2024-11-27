from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import qrcode
import os
import random

app = Flask(__name__)

# 애플리케이션의 비밀 키 설정. 세션을 암호화하는 데 사용됨.
app.secret_key = '@@@'

# 게임 데이터 설정

games = {
    'Game 1': {
        'redwonbin.jpg': 0,
        'hairgwanggyu.jpg': 0
    },
    'Game 2': {
        'body.jpg': 0,
        'face.jpg': 0
    },
    'Game 3': {
        'memory.jpg': 0,
        '71.jpg': 0
    },
    'Game 4': {
        'redkarina.jpg': 0,
        'winter.jpg': 0
    },
    'Game 5': {
        'songface.jpg': 0,
        'lee.jpg': 0
    },
    'Game 6': {
        'now.jpg' : 0,
        '1000million.jpg' : 0
    },
    'Game 7': {
        'rebirth_female.jpg' : 0,
        'rebirth_male.jpg' : 0
    },
    'Game 8': {
        '2seul.jpg' : 0,
        '1jin.jpg' : 0
    },
    'Game 9': {
        'yoajung.jpg' : 0,
        'sulbing.jpg' : 0
    },
    'Game 10': {
        'empty_brain.jpg' : 0,
        'skinhead.jpg' : 0
    },
}

# 게임 순서 설정
game_sequence = random.sample(list(games.keys()), 5)

# 사용자별 게임 상태 저장을 위한 딕셔너리

user_games = {}
# 완료된 사용자 수
completed_users = 0

# 메인 페이지
@app.route('/')
def main_page():
    return render_template('main.html')

# 게임 시작 처리
@app.route('/start')
def start_game():
    ip_address = request.remote_addr  # 사용자의 IP 주소 가져오기
    
    # 사용자의 게임 상태가 없으면 초기화
    if ip_address not in user_games:
        user_games[ip_address] = {'current_game': 0}

    return redirect(url_for('index'))

# 게임 페이지
@app.route('/game')
def index():
    ip_address = request.remote_addr  # 사용자의 IP 주소 가져오기
    
    # IP 주소가 없으면 초기화
    if ip_address not in user_games:
        user_games[ip_address] = {'current_game': 0}

    # 현재 게임 인덱스를 가져옴
    current_game_index = user_games[ip_address]['current_game']
    
    # 현재 게임 인덱스가 범위를 초과할 경우 종료 페이지로 리다이렉트
    if current_game_index >= len(game_sequence):
        return redirect(url_for('end'))

    game = game_sequence[current_game_index]
    return render_template('index.html', game=game, images=list(games[game].keys()), current_game_index=current_game_index)

# 투표 처리
@app.route('/vote', methods=['POST'])
def vote():
    global completed_users
    ip_address = request.remote_addr  # 사용자의 IP 주소 가져오기
    game = request.form['game']  # 폼에서 선택된 게임
    choice = request.form['choice']  # 폼에서 선택된 이미지 선택지

    # 사용자가 현재 게임을 가지고 있으면 투표 처리
    if ip_address in user_games:
        current_game_index = user_games[ip_address]['current_game']
        
        # 현재 게임 인덱스가 범위를 초과할 경우 처리
        if current_game_index >= len(game_sequence):
            return redirect(url_for('end'))

        game_to_play = game_sequence[current_game_index]

        # 선택한 게임과 현재 게임이 일치하고, 선택지가 유효하면 투표 처리
        if game == game_to_play and choice in games[game_to_play]:
            games[game_to_play][choice] += 1  # 선택된 이미지의 투표 수 증가

            # 사용자가 선택한 게임과 선택한 옵션을 user_games에 저장
            if 'voted_choices' not in user_games[ip_address]:
                user_games[ip_address]['voted_choices'] = {}
            user_games[ip_address]['voted_choices'][game] = choice  # 해당 게임에서 선택한 옵션 저장

        # 현재 게임 상태 업데이트
        user_games[ip_address]['current_game'] += 1

        # 사용자가 마지막 게임을 완료하면 완료된 사용자 수 증가
        if user_games[ip_address]['current_game'] >= len(game_sequence):
            completed_users += 1
            return redirect(url_for('end'))  # 마지막 게임 후 결과 페이지로 리다이렉트
        else:
            return redirect(url_for('index'))  # 다음 게임으로 이동

    return redirect(url_for('index'))

# '뒤로가기' 처리
@app.route('/back', methods=['POST'])
def go_back():
    ip_address = request.remote_addr  # 사용자의 IP 주소 가져오기
    
    if ip_address in user_games:
        current_game_index = user_games[ip_address]['current_game']
        
        if current_game_index > 0:  # 첫 번째 게임이 아닌 경우에만 뒤로 가기 허용
            # 현재 게임의 투표 수를 감소시킨다 (이전 선택지로 돌아갈 때)
            previous_game = game_sequence[current_game_index - 1]  # 이전 게임 이름 가져오기
            if previous_game in user_games[ip_address]['voted_choices']:
                previous_choice = user_games[ip_address]['voted_choices'][previous_game]
                games[previous_game][previous_choice] -= 1  # 이전 선택지의 투표 수 감소

            user_games[ip_address]['current_game'] -= 1  # 현재 게임 인덱스 감소

            # 이전 게임의 선택지를 초기화 (다시 선택 가능하게)
            if previous_game in user_games[ip_address]['voted_choices']:
                del user_games[ip_address]['voted_choices'][previous_game]  # 이전에 선택한 것을 삭제

    return redirect(url_for('index'))

# 게임 데이터를 JSON 형태로 반환
@app.route('/update_data', methods=['GET'])
def update_data():
    return jsonify(games) # 게임 데이터를 JSON으로 반환

# 게임 종료
@app.route('/end')
def end():
    return render_template('end.html', game_sequence=game_sequence)

# 관리자 페이지 비밀번호
PASSWORD = "0000"

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    # POST 요청일 때 비밀번호 확인 처리
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:  # 비밀번호가 맞으면 세션에 인증 상태 저장
            session['authenticated'] = True 
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid password")

    return render_template('admin_login.html')

# 관리자 대시보드
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('authenticated'): # 인증된 사용자만 접근할 수 있도록 세션 체크
        return redirect(url_for('admin_page'))
    
    # 공용 IP 주소 설정
    public_ip_address = "@@@@"  # 공용 IP 주소
    
    # QR 코드 생성
    img = qrcode.make(f"http://{public_ip_address}:80")  # QR 코드에 공용 IP 주소 사용
    qr_code_path = "static/admin_qr_code.png"  # QR 코드 파일 경로
    img.save(qr_code_path)  # QR 코드 파일로 저장
    
    return render_template('admin.html', games=games, completed_users=completed_users, game_sequence=game_sequence)  # 관리자 대시보드 페이지 렌더링

# 관리자 상태를 JSON 형태로 반환
@app.route('/admin_status')
def admin_status():
    return jsonify({'completed': completed_users})

# 모든 사용자 정보 초기화 처리
@app.route('/reset_users', methods=['POST'])
def reset_users():
    global user_games, completed_users

    # 사용자 게임 상태 초기화
    user_games = {}
    completed_users = 0

    # 게임 데이터도 초기화하고 싶다면 아래 코드를 추가할 수 있습니다.
    for game in games:
        for image in games[game]:
            games[game][image] = 0

    return redirect(url_for('admin_dashboard'))


# 게임 종료 처리
@app.route('/end_game', methods=['POST'])
def end_game():
    global completed_users
    ip_address = request.remote_addr  # 사용자의 IP 주소 가져오기
    
    if ip_address in user_games:
        user_games[ip_address]['current_game'] = len(game_sequence)  # 현재 게임을 마지막으로 설정하여 게임 종료
        completed_users += 1  # 완료된 사용자 수 증가

@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    public_ip_address = "@@@@"
    
    # 종료 페이지에 대한 QR 코드 생성
    img = qrcode.make(f"http://{public_ip_address}/end")  
    qr_code_path = "static/end_qr_code.png"  # QR 코드 파일 경로
    img.save(qr_code_path)  # QR 코드를 파일로 저장
    
    return jsonify({"success": True, "qr_code_url": qr_code_path})

    # QR 코드 생성 (종료 페이지로 리다이렉트)
    # 공용 IP 주소 설정
    public_ip_address = "@@@"
    img = qrcode.make(f"http://{public_ip_address}/end")  # 종료 페이지에 대한 QR 코드 생성
    qr_code_path = "static/end_qr_code.png"  # QR 코드 파일 경로
    img.save(qr_code_path)  # QR 코드를 파일로 저장

    return jsonify({"success": True, "qr_code_url": qr_code_path})

if __name__ == '__main__':
    app.run(host='@@@', port=@@, debug=True)
