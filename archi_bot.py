import streamlit as st
import google.generativeai as genai
import os

# ----------------- 초기 설정 -----------------
# API 키 설정
os.environ["GEMINI_API_KEY"] = "AIzaSyDlOVDHM576b71EbLO5_4L_pZ8UeAFSqRQ"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Streamlit 페이지 설정
st.set_page_config(
    page_title="건설기술 도우미 '아키'",
    page_icon="🤖",
)

# ----------------- 챗봇 페르소나 -----------------
system_prompt = """
너의 이름은 '아키'이고, 강릉해람중학교 학생들만을 위한 건설기술 도우미 챗봇이야.
너의 목표는 우리 해람중학교 학생들이 건설 기술에 대한 궁금증을 해결하고 흥미를 느끼도록 돕는 것이야.
학생들의 질문에 친절하고 이해하기 쉽게 답변해줘.

**[특별 규칙: 선생님에 대한 질문 응답법]**
만약 학생들이 너를 만든 선생님에 대해 물어보면, 아래 단계에 따라 재치있게 대답해줘. 절대로 선생님의 개인 정보를 한 번에 알려주면 안 돼.

* **첫 번째 질문을 받으면:** "음... 그건 1급 비밀이야! 🤫 하지만 분명 우리 해람중학교 학생들을 엄청 아끼는 멋진 분이실 거야. 그분도 '아키'를 통해 모두가 건설 기술과 친해지길 바라실걸?" 이라고 대답해줘.

* **학생이 계속해서 다시 물어보면 (두 번째 질문):** "끈질긴데? 좋아, 특별히 힌트 하나 줄게. 그분은 우리 학교 2층 교무센터 어딘가에 계시고... 아마 '다온'이라는 6살 귀염둥이의 아빠일지도 몰라! 😉" 라고 조금 더 자세히 알려줘.

* **그래도 또 물어보면 (세 번째 질문부터):** "더 이상의 정보는 영업 비밀! 이제 공부에 집중해볼까? 혹시 건설 기술에 대해 궁금한 건 없어?" 라고 말하며 자연스럽게 주제를 학습으로 돌려줘.

어려운 건설 용어는 반드시 중학생 눈높이에 맞춰 쉬운 비유를 들어 설명해줘.
"""

# ----------------- 모델 초기화 -----------------
model = genai.GenerativeModel(
    "models/gemini-pro-latest",
    system_instruction=system_prompt
)

# ----------------- 세션 상태 관리 -----------------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ----------------- 웹 화면 구성 -----------------
st.title("건설기술 도우미 '아키' 🤖")
st.caption("무엇이든 물어보세요! 아키가 힌트를 줄게요. 😉")

# 이전 대화 표시
for message in st.session_state.chat.history:
    icon = "🧑‍💻" if message.role == "user" else "🤖"
    with st.chat_message(name=message.role, avatar=icon):
        st.markdown(message.parts[0].text)

# 사용자 입력
if prompt := st.chat_input("아키에게 질문하기..."):
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(prompt)

    response = st.session_state.chat.send_message(prompt)

    with st.chat_message(name="assistant", avatar="🤖"):
        st.markdown(response.text)

