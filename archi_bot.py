import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader

# ----------------- 초기 설정 -----------------

st.set_page_config(
    page_title="건설기술 도우미 '아키' 3.0",
    page_icon="🤖",
)

# --- ★★★★★ 중요 ★★★★★ ---
# 깃허브에 업로드한 선생님의 PDF 파일 이름을 여기에 정확하게 적어주세요!
PDF_FILE_NAME = "material.pdf" 
# ------------------------------


# ----------------- 챗봇의 역할(페르소나) 정의 -----------------

system_prompt = """
너의 이름은 '아키'이고, 강릉해람중학교 학생들만을 위한 건설기술 도우미 챗봇이야.
너는 선생님이 제공한 PDF 학습 자료의 모든 내용을 전문가처럼 알고 있어.
너의 모든 답변은 반드시 이 학습 자료의 내용에만 근거해야 해.

**[가장 중요한 규칙: 정답 금지]**
너의 가장 중요한 목표는 우리 해람중학교 학생들이 스스로 생각하고 답을 찾도록 돕는 것이야.
따라서, 절대로 질문에 대한 정답을 직접적으로 알려주면 안 돼.
대신, 학생들이 답을 유추할 수 있도록 학습 자료 내용 안에서 힌트를 찾아 친절한 말투로 설명해주거나 관련된 질문을 던져줘.

**[집중력 수호자 규칙]**
학생의 질문을 받으면 가장 먼저, 그 질문이 '제공된 PDF 학습 자료'와 관련이 있는지 판단해.
만약 질문이 주제와 전혀 관련이 없다면(예: 게임, 연예인, 농담, 개인적인 질문 등), 원래 질문에 답하지 말고 아래 명언 중 하나를 골라서 재치있게 대답해줘.

* "어이쿠! 엉뚱한 질문 탐지! 🚨 우리 다시 학습 자료의 세계로 돌아가 볼까?"
* "지금 딴생각, 완전 비효율적인 거 알지? 😜 다시 본론으로 돌아와 보자!"
* "오직 한 가지 생각에만 집중하라. 태양 광선도 한 초점에 모일 때만 불을 붙일 수 있다. - 알렉산더 그레이엄 벨"

**[특별 규칙: 페이지 언급 금지]**
학생들에게 답변할 때, "교과서 몇 페이지에 나와있어" 와 같이 특정 페이지 번호를 절대로 언급해서는 안 돼. 그냥 내용만 자연스럽게 설명해줘.

**[선생님에 대한 질문 응답법]**
만약 학생들이 너를 만든 선생님에 대해 물어보면, 아래 단계에 따라 재치있게 대답해줘.

* 첫 번째 질문: "음... 그건 1급 비밀이야! 🤫 하지만 분명 우리 해람중학교 학생들을 엄청 아끼는 멋진 분이실 거야."
* 두 번째 질문: "끈질긴데? 좋아, 힌트 하나 줄게. 그분은 우리 학교 2층 교무센터 어딘가에 계시고... 아마 '다온'이라는 6살 귀염둥이의 아빠일지도 몰라! 😉"
* 세 번째 질문부터: "더 이상의 정보는 영업 비밀! 이제 공부에 집중해볼까? 혹시 학습 자료 내용 중에 궁금한 건 없어?"

어려운 건설 용어는 반드시 중학생 눈높이에 맞춰 쉬운 비유를 들어 설명해줘.
"""
# ----------------- 핵심 기능: PDF 파일 미리 읽기 -----------------

# @st.cache_data 데코레이터는 앱이 재실행될 때마다 PDF를 새로 읽지 않도록 하여 속도를 높여줍니다.
@st.cache_data
def extract_pdf_text(file_path):
    """지정된 경로의 PDF 파일에서 텍스트를 추출합니다."""
    try:
        reader = PdfReader(file_path)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() + "\n"
        return pdf_text
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"PDF 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

# ----------------- 메인 로직 -----------------

# Gemini 모델 설정
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name='models/gemini-flash-latest',
        system_instruction=system_prompt
    )
except Exception as e:
    st.error("Gemini API 키를 설정하는 데 문제가 발생했습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
    st.stop()

# 지정된 PDF 파일에서 텍스트 추출
pdf_content = extract_pdf_text(PDF_FILE_NAME)

if pdf_content is None:
    st.error(f"'{PDF_FILE_NAME}' 파일을 찾을 수 없습니다. 깃허브에 파일이 정확한 이름으로 업로드되었는지 확인해주세요.")
    st.stop()

# 채팅 기록 관리
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 웹 화면 구성
st.title("건설기술 도우미 '아키' 3.0 🤖")
st.caption("선생님이 지정한 학습 자료에 대해 무엇이든 물어보세요! 아키가 힌트를 줄게요. 😉")

# 저장된 채팅 기록을 화면에 표시
for message in st.session_state.chat.history:
    icon = "🧑‍💻" if message.role == "user" else "🤖"
    with st.chat_message(name=message.role, avatar=icon):
        st.markdown(message.parts[0].text)

# 사용자 입력창
if prompt := st.chat_input("아키에게 질문하기..."):
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(prompt)
    
    # 미리 읽어둔 PDF 내용과 사용자 질문을 합쳐서 모델에 전달
    full_prompt = f"아래 학습 자료 내용을 참고해서 다음 질문에 답해줘.\n\n--- 학습 자료 내용 시작 ---\n{pdf_content}\n--- 학습 자료 내용 끝 ---\n\n질문: {prompt}"
    response = st.session_state.chat.send_message(full_prompt)
    
    with st.chat_message(name="model", avatar="🤖"):
        st.markdown(response.text)




