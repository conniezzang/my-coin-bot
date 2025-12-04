import streamlit as st
import requests
import time

# 페이지 설정
st.set_page_config(page_title="코인 봇 로그인", page_icon="🔒", layout="centered")

# ==========================================
# 1. 로그인 화면 함수
# ==========================================
def login_page():
    st.title("🔒 로그인")
    st.write("관리자 승인이 필요합니다.")

    with st.form("login_form"):
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        submit = st.form_submit_button("로그인")

        if submit:
            # secrets.toml 파일에 있는 아이디/비번과 비교
            if username in st.secrets["passwords"] and st.secrets["passwords"][username] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("로그인 성공!")
                time.sleep(0.5)
                st.rerun()  # 화면 새로고침
            else:
                st.error("아이디 또는 비밀번호가 틀렸습니다.")

# ==========================================
# 2. 메인 대시보드 함수 (아까 만든 그 코드)
# ==========================================
def main_page():
    st.title(f"👋 환영합니다, {st.session_state['username']}님!")
    
    # [수정된 부분] 서버 주소를 입력받는 칸 추가
    st.info("💡 서버 연결 설정")
    server_url = st.text_input("서버 URL 입력 (ngrok 주소)", value="https://xxxx-xxxx.ngrok-free.app")
    
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🎮 조작 패널")
        ticker = st.text_input("코인 티커", value="BTC/USDT")
        qty = st.number_input("주문 수량", value=0.001, format="%.4f")
        
        # 버튼을 누르면 입력한 server_url로 신호를 보냄
        if st.button("🔵 롱 (Buy) 테스트"):
            try:
                # url 뒤에 /webhook을 붙여서 완성
                target_url = f"{server_url.rstrip('/')}/webhook"
                payload = {"ticker": ticker, "action": "buy", "quantity": qty}
                
                res = requests.post(target_url, json=payload)
                if res.status_code == 200: st.success("성공")
                else: st.error("실패")
            except Exception as e: st.error(f"에러: {e}")

        if st.button("🔴 숏 (Sell) 테스트"):
            try:
                target_url = f"{server_url.rstrip('/')}/webhook"
                payload = {"ticker": ticker, "action": "sell", "quantity": qty}
                
                res = requests.post(target_url, json=payload)
                if res.status_code == 200: st.success("성공")
                else: st.error("실패")
            except Exception as e: st.error(f"에러: {e}")

    with col2:
        st.subheader("📜 로그 확인")
        st.caption("보안상 클라우드 버전에서는 로그 파일 직접 보기가 제한될 수 있습니다.")
        # (클라우드에서는 내 컴퓨터의 logs.txt를 직접 읽을 수 없습니다. 
        # 이 기능은 나중에 'API로 로그 요청하기' 기능을 추가해야 합니다. 지금은 일단 비워둡니다.)

# ==========================================
# 3. 프로그램 시작점 (문지기 역할)
# ==========================================
# 'logged_in'이라는 통행증이 없으면 False로 설정
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 통행증 확인
if st.session_state["logged_in"]:
    main_page()  # 통행증 있으면 메인 화면 보여줌
else:
    login_page() # 없으면 로그인 화면 보여줌