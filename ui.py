import streamlit as st
import requests

st.set_page_config(page_title="공용 코인 봇", page_icon="🏦")

st.title("🏦 비트겟 친구들 전용 봇")

# ==========================================
# 1. 왼쪽 사이드바: 개인 정보 입력
# ==========================================
with st.sidebar:
    st.header("🔑 내 계정 정보 입력")
    st.info("비트겟 API 키를 입력하세요. (저장되지 않습니다)")
    
    # 비밀번호처럼 보이게 type="password" 설정
    user_api_key = st.text_input("Access Key", type="password")
    user_secret = st.text_input("Secret Key", type="password")
    user_password = st.text_input("Passphrase", type="password")
    
    st.divider()
    
    st.header("⚙️ 서버 설정")
    # ngrok 주소 입력
    server_url = st.text_input("봇 서버 URL", value="https://xxxx-xxxx.ngrok-free.app")


# ==========================================
# 2. 메인 화면: 매매 버튼
# ==========================================
st.subheader("🎮 주문 패널")

col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input("코인 티커", value="BTC/USDT")
with col2:
    qty = st.number_input("주문 수량", value=0.001, format="%.4f")

st.markdown("---")

# 매매 함수 (키를 묶어서 보냄)
def send_order(action_type):
    # 키가 입력 안 됐으면 경고
    if not user_api_key or not user_secret or not user_password:
        st.error("⚠️ 왼쪽 사이드바에 API 키를 먼저 입력해주세요!")
        return

    payload = {
        "apiKey": user_api_key,
        "secret": user_secret,
        "password": user_password,
        "ticker": ticker,
        "action": action_type,
        "quantity": qty
    }
    
    try:
        url = f"{server_url.rstrip('/')}/webhook"
        res = requests.post(url, json=payload)
        
        if res.status_code == 200:
            st.success(f"{action_type} 주문 성공!")
            st.balloons()
        else:
            st.error(f"주문 실패: {res.text}")
    except Exception as e:
        st.error(f"서버 연결 오류: {e}")

# 버튼 배치
if st.button("🔵 롱 (Long) 진입", use_container_width=True):
    send_order("buy")

if st.button("🔴 숏 (Short) 진입", use_container_width=True):
    send_order("sell")