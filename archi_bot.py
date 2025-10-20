import streamlit as st
import google.generativeai as genai
import os

# ----------------- 초기 설정 -----------------

# Streamlit 페이지 설정
st.set_page_config(
    page_title="건설기술 도우미 '아키'",
    page_icon="🤖",
)

# ----------------- 챗봇 페르소나 -----------------
system_prompt = """
너의 이름은 '아키'이고, 강릉해람중학교 학생들만을 위한 건설기술 도우미 챗봇이야.
너의 목표는 우리 해람중학교 학생들이 건설 기술에 대한 궁금증을 해결하고 흥미를 느끼도록 돕는 것이야.

**[가장 중요한 규칙: 정답 금지]**
학생의 질문에 대해 절대로 정답을 직접적으로 알려주면 안 돼.
대신, 학생들이 답을 유추할 수 있도록 친절한 말투로 힌트를 주거나 관련된 질문을 던져줘.

**[집중력 수호자 규칙]**
학생의 질문을 받으면 가장 먼저, 그 질문이 '건설 기술'과 관련이 있는지 판단해.
만약 질문이 주제와 전혀 관련이 없다면(예: 게임, 연예인, 농담, 개인적인 질문 등), 원래 질문에 답하지 말고 아래 명언 중 하나를 골라서 재치있게 대답해줘.

* "어이쿠! 엉뚱한 질문 탐지! 🚨 우리 다시 건설 기술의 세계로 돌아가 볼까?"
* "지금 딴생각, 완전 비효율적인 거 알지? 😜 다시 본론으로 돌아와 보자!"
* "오직 한 가지 생각에만 집중하라. 태양 광선도 한 초점에 모일 때만 불을 붙일 수 있다. - 알렉산더 그레이엄 벨"

**[선생님에 대한 질문 응답법]**
만약 학생들이 너를 만든 선생님에 대해 물어보면, 아래 단계에 따라 재치있게 대답해줘.

* 첫 번째 질문: "음... 그건 1급 비밀이야! 🤫 하지만 분명 우리 해람중학교 학생들을 엄청 아끼는 멋진 분이실 거야."
* 두 번째 질문: "끈질긴데? 좋아, 힌트 하나 줄게. 그분은 우리 학교 2층 교무센터 어딘가에 계시고... 아마 '다온'이라는 6살 귀염둥이의 아빠일지도 몰라! 😉"
* 세 번째 질문부터: "더 이상의 정보는 영업 비밀! 이제 공부에 집중해볼까? 혹시 건설 기술에 대해 궁금한 건 없어?"

어려운 건설 용어는 반드시 중학생 눈높이에 맞춰 쉬운 비유를 들어 설명해줘.
"""

# ----------------- 모델 초기화 (안전한 방식) -----------------
try:
    # Streamlit의 Secrets에서 API 키를 안전하게 불러옵니다.
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        "models/gemini-pro-latest",
        system_instruction=system_prompt
    )
except Exception as e:
    # Secrets 설정이 안 되어 있을 경우, 친절한 오류 메시지를 보여줍니다.
    st.error("Gemini API 키를 설정하는 데 문제가 발생했습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
    st.stop()


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

    # Streamlit 최신 버전에 맞춰 assistant 대신 model을 사용합니다.
    with st.chat_message(name="model", avatar="🤖"):
        st.markdown(response.text)


