import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API 키 없음")

model = init_chat_model(
    model_provider="openai",
    model="gpt-4o-mini",
    api_key=api_key
)

response = model.invoke("안녕하세요. 간단한 자기소개 해주세요.")
print(response.text)