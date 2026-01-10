import streamlit as st
import time
import requests
import random
import json
from datetime import datetime
import os

# ==========================================
# 사용자 설정
# ==========================================
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
ORDERS_FILE = "orders_history.json"

# ==========================================
# 데이터 저장/불러오기
# ==========================================
def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_order(order):
    orders = load_orders()
    orders.append(order)
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

# ==========================================
# 텔레그램 발송
# ==========================================
def send_telegram_msg(item, address, cost, order_num):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    message = f"""
🎊 **Universe Store 주문 영수증**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 **상품명:** {item}
🏷️ **주문번호:** {order_num}
🏠 **배송지:** {address}
💳 **결제수단:** Universe Card (NH 연동)
💰 **결제금액:** {cost}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ **결제완료**
🚀 **배송상태:** 배송 시작됨

⏰ 예상 도착: 타임라인에 이미 도착함
📱 추적: 믿음의 강도에 따라 자동 업데이트

**It is done. 이미 당신의 것입니다.**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💌 Universe Fulfillment Center
    """
    
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except:
        pass

# ==========================================
# 인기 상품 카탈로그
# ==========================================
CATALOG = {
    "💰 월 수익 5,000만원": {
        "desc": "안정적인 현금흐름 | ⭐⭐⭐⭐⭐ (9,847명 리뷰)",
        "price": "늘 감사함",
        "emoji": "💰"
    },
    "❤️ 방님과의 사랑": {
        "desc": "영혼의 파트너 | ⭐⭐⭐⭐⭐ (7,231명 리뷰)",
        "price": "자기 사랑",
        "emoji": "❤️"
    },
    "💪 건강한 몸": {
        "desc": "에너지 넘치는 삶 | ⭐⭐⭐⭐⭐ (12,441명 리뷰)",
        "price": "자기 존중 관리",
        "emoji": "💪"
    },
    "🏠 꿈의 집": {
        "desc": "완벽한 공간 | ⭐⭐⭐⭐⭐ (5,392명 리뷰)",
        "price": "안정감 평화로움",
        "emoji": "🏠"
    },
    "✈️ 자유로운 여행 라이프": {
        "desc": "시간과 경제 자유 | ⭐⭐⭐⭐⭐ (8,129명 리뷰)",
        "price": "감사함의 확장",
        "emoji": "✈️"
    },
    "🎯 직접 입력": {
        "desc": "원하는 것을 직접 주문하세요",
        "price": "커스텀 가격",
        "emoji": "🎯"
    }
}

# ==========================================
# CSS 스타일링
# ==========================================
st.set_page_config(
    page_title="Universe Store 🌌",
    page_icon="🌌",
    layout="wide"
)

st.markdown("""
<style>
    .product-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .product-card:hover {
        transform: translateY(-5px);
    }
    .order-number {
        font-size: 24px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 페이지 네비게이션
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.sidebar.title("🌌 Universe Store")
menu = st.sidebar.radio("메뉴", ["🏠 홈", "🛒 주문하기", "📦 주문내역", "ℹ️ 이용안내"])

if menu == "🏠 홈":
    st.session_state.page = 'home'
elif menu == "🛒 주문하기":
    st.session_state.page = 'order'
elif menu == "📦 주문내역":
    st.session_state.page = 'history'
elif menu == "ℹ️ 이용안내":
    st.session_state.page = 'info'

# ==========================================
# 홈 페이지
# ==========================================
if st.session_state.page == 'home':
    st.title("🌌 Universe Fulfillment Center")
    st.markdown("### ✨ 당신이 원하는 모든 것, 이미 준비되어 있습니다")
    
    st.info("💫 **오늘의 특가:** 모든 상품 우주 무료배송 | 🎁 첫 주문 고객 특별 선물")
    
    st.markdown("---")
    st.subheader("🔥 베스트셀러 Top 5")
    
    cols = st.columns(3)
    for idx, (product, info) in enumerate(list(CATALOG.items())[:5]):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <h3>{info['emoji']} {product.replace(info['emoji'], '').strip()}</h3>
                <p>{info['desc']}</p>
                <p><strong>💳 Price:</strong> {info['price']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🛒 지금 주문하기", type="primary", use_container_width=True):
        st.session_state.page = 'order'
        st.rerun()

# ==========================================
# 주문 페이지
# ==========================================
elif st.session_state.page == 'order':
    st.title("🛒 주문하기")
    
    st.subheader("1️⃣ 상품 선택")
    selected_product = st.selectbox(
        "원하는 상품을 선택하세요",
        list(CATALOG.keys()),
        format_func=lambda x: f"{CATALOG[x]['emoji']} {x}"
    )
    
    if "직접 입력" in selected_product:
        desired_item = st.text_input("🎯 원하는 것을 구체적으로 입력하세요", 
                                     placeholder="예: 해외선물로 월 15만불")
    else:
        desired_item = selected_product
    
    st.markdown("---")
    
    st.subheader("2️⃣ 배송 정보")
    col1, col2 = st.columns(2)
    with col1:
        address = st.text_input("🏠 받으실 곳", 
                               placeholder="지금의 나, 2026년의 나")
    with col2:
        receiver_state = st.selectbox("💫 현재 마음 상태", 
                                     ["이미 받은 안도감", "감사하는 마음", "평온한 확신"])
    
    st.markdown("---")
    
    st.subheader("3️⃣ 결제 정보")
    payment_method = st.selectbox("💳 결제 수단", 
                                  ["Universe Card (NH농협은행)", "포인트", "자동이체"])
    
    with st.expander("💳 카드 정보 입력 (보안 연결됨 🔒)"):
        card_num = st.text_input("카드 번호", placeholder="1234-5678-9012-3456", max_chars=19)
        col1, col2 = st.columns(2)
        with col1:
            expiry = st.text_input("유효기간 (MM/YY)", placeholder="12/28")
        with col2:
            cvv = st.text_input("CVV", type="password", placeholder="***", max_chars=3)
    
    price_display = CATALOG[selected_product]['price'] if "직접 입력" not in selected_product else "이미 완료"
    st.info(f"💰 **결제 금액:** {price_display} (이미 지불됨)")
    
    st.warning("⚠️ 이 주문은 취소할 수 없으며, 우주 법칙에 따라 반드시 배송됩니다.")
    
    st.markdown("---")
    agree = st.checkbox("위 내용을 확인했으며, 우주의 배송을 신뢰합니다 ✨")
    
    if st.button("🎊 최종 주문하기", type="primary", disabled=not agree, use_container_width=True):
        if not desired_item or not address:
            st.error("❌ 상품명과 배송지를 모두 입력해주세요!")
        else:
            status_container = st.empty()
            progress_bar = st.progress(0)
            
            steps = [
                ("💳 카드 정보 확인 중...", 15),
                ("🏦 결제 승인 요청 중...", 30),
                ("✅ 결제 승인 완료", 50),
                ("🌌 우주 재고 확인 중...", 70),
                ("📦 상품 포장 중...", 85),
                ("🚀 우주 배송 시작...", 100),
            ]
            
            for step, progress in steps:
                status_container.info(step)
                progress_bar.progress(progress)
                time.sleep(1)
            
            if random.random() < 0.05:
                status_container.error("⚠️ 일시적 오류 발생. 재시도 중...")
                time.sleep(2)
                status_container.success("✅ 재시도 성공!")
            
            order_num = f"UNIVERSE-{int(time.time())}"
            
            st.balloons()
            st.success("🎉 주문이 성공적으로 완료되었습니다!")
            
            st.markdown(f"""
            <div class="order-number">
                📋 주문번호: {order_num}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            ### ✅ 주문 완료
            - **상품:** {desired_item}
            - **배송지:** {address}
            - **마음 상태:** {receiver_state}
            - **결제 수단:** {payment_method}
            
            ---
            
            ### 🚀 배송 진행 상황
            """)
            
            delivery_steps = [
                ("✅ 주문 접수 완료", True),
                ("✅ 우주 창고 출발", True),
                ("🔄 양자 터널 통과 중", True),
                ("⏳ 현실화 프로세스 진행 중", False),
                ("📍 배송 완료 (타임라인 도착)", False)
            ]
            
            for step, completed in delivery_steps:
                if completed:
                    st.success(step)
                else:
                    st.info(step)
            
            st.markdown("---")
            st.info("💌 잠시 후 텔레그램으로 영수증이 발송됩니다.")
            st.markdown("**💡 Tip:** 이제 주문을 잊고 천천히 일상을 즐기세요. 배송은 이미 완료되었습니다.")
            
            order_data = {
                "order_num": order_num,
                "item": desired_item,
                "address": address,
                "state": receiver_state,
                "price": price_display,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "배송 중 🚀"
            }
            save_order(order_data)
            
            try:
                send_telegram_msg(desired_item, address, price_display, order_num)
            except Exception as e:
                st.warning(f"텔레그램 전송 오류: {e}")

# ==========================================
# 주문 내역 페이지
# ==========================================
elif st.session_state.page == 'history':
    st.title("📦 주문 내역")
    
    orders = load_orders()
    
    if not orders:
        st.info("아직 주문 내역이 없습니다. 첫 주문을 시작해보세요! 🛒")
    else:
        st.markdown(f"**총 {len(orders)}개의 주문**")
        st.markdown("---")
        
        for order in reversed(orders):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"### 📦 {order['item']}")
                    st.caption(f"주문번호: {order['order_num']}")
                
                with col2:
                    st.markdown(f"**배송지:** {order['address']}")
                    st.caption(f"주문일: {order['date']}")
                
                with col3:
                    st.markdown(f"**{order['status']}**")
                
                st.markdown("---")

# ==========================================
# 이용안내 페이지
# ==========================================
elif st.session_state.page == 'info':
    st.title("ℹ️ Universe Store 이용 안내")
    
    st.markdown("""
    ## 🌌 Universe Store란?
    
    당신이 원하는 모든 것이 이미 우주 창고에 준비되어 있습니다.
    주문만 하면, 시공간을 초월한 배송이 시작됩니다.
    
    ---
    
    ## 📋 이용 방법
    
    1. **상품 선택:** 원하는 것을 명확하게 선택하세요
    2. **배송지 입력:** 현재의 당신 상태를 입력하세요
    3. **결제:** 이미 지불되어 있습니다 (확고한 믿음으로)
    4. **배송 대기:** 잊고 살아가세요. 자동으로 도착합니다
    
    ---
    
    ## 🚀 배송 정책
    
    - **배송 기간:** 이미 도착함
    - **배송 방식:** 양자 터널 직배송
    - **추적:** 믿음의 강도로 자동 업데이트
    - **환불:** 불가 (우주 법칙)
    
    ---
    
    *"All is done. 이미 나의 것입니다."*
    """)

st.sidebar.markdown("---")
st.sidebar.info("""
💫 **Today's Quote**

"당신이 주문한 순간,
우주는 이미 배송을 시작했습니다."
""")

st.sidebar.markdown("---")
st.sidebar.caption("🌌 Universe Store v2.0")
st.sidebar.caption("Powered by Quantum Delivery")
