from langchain.chat_models import init_chat_model
from langchain_core.prompts import load_prompt
from openai import api_key

from my_agent.config import get_settings


model = init_chat_model(model_provider="openai", model="gpt-5.2", api_key=get_settings().openai_api_key)
prompt = load_prompt("src/prompts/email_summary.yaml")

chain = prompt | model
response = chain.invoke(input={
    "email": """
안녕하세요. ABC테크 개발팀 김민수입니다.

테스트 프로젝트 Alpha의 배포 일정이 기존 11월 20일에서 **11월 25일로 변경**되었습니다.

QA 과정에서 로그인 오류와 알림 중복 수신 문제가 발견되어 추가 수정이 필요한 상황입니다.

각 팀에서는 아래 사항을 확인해 주세요.

- 개발팀: 11월 19일까지 오류 수정 완료
- QA팀: 11월 22일까지 재검증 진행
- 기획팀: 11월 20일까지 변경 사항 검토

단, QA 결과에 따라 배포 일정이 추가로 변경될 수 있습니다.

일정에 문제가 있는 담당자는 11월 18일 오후 3시까지 회신 부탁드립니다.

감사합니다.

김민수 드림  
ABC테크 개발팀
"""
})

print(response.text)