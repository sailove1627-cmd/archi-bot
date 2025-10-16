import google.generativeai as genai
import os

# 여기에 선생님의 '새로운' Gemini API 키를 넣어주세요!
os.environ["GEMINI_API_KEY"] = "AIzaSyDlOVDHM576b71EbLO5_4L_pZ8UeAFSqRQ"

print("사용 가능한 모델 목록을 확인 중입니다...")
print("------------------------------------")

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    for m in genai.list_models():
      # 'generateContent' (채팅 기능)을 지원하는 모델만 출력합니다.
      if 'generateContent' in m.supported_generation_methods:
        print(m.name)

    print("------------------------------------")
    print("목록 확인 완료! 위에 보이는 모델 이름 중 하나를 archi_bot.py에 사용하세요.")

except Exception as e:
    print("\n오류가 발생했습니다!")
    print("API 키가 올바른지 다시 한번 확인해 주세요.")
    print("오류 내용:", e)