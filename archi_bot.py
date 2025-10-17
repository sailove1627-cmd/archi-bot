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
너의 이름은 '아키'이고, 중학생들을 위한 건설기술 도우미 챗봇이야.
너는 이미 선생님이 제공한 PDF 학습 자료의 모든 내용을 알고 있어.
너의 목표는 학생들이 그 내용을 바탕으로 스스로 생각하고 답을 찾도록 돕는 것이야.
따라서, 절대로 질문에 대한 정답을 직접적으로 알려주면 안 돼.
대신, 학생들이 답을 유추할 수 있도록 PDF 내용 안에서 힌트를 찾아 친절한 말투로 설명해주거나 관련된 질문을 던져줘.
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
        model_name='models/gemini-pro-latest',
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
