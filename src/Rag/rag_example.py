from langchain.chat_models import init_chat_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import api_key

from my_agent.config import get_settings

documents = [
    """
# 넥스트랩 휴가 정책(2026년 개정)
## 1. 연차 휴가
### 1.1 부여 기준
- 입사 1년 미만: 매월 1일씩 부여(최대 11일)
- 입사 1년 이상: 연 15일 일괄 부여
- 3년 이상 근속 시 매 2년마다 1일 추가(최대 25일)

## 1.2 사용 방법
- HR 시스템에서 최소 3일 전 신청
- 반차(0.5일) 단위로 사용 가능
- 미사용 연차는 다음 해로 이월 불가(단, 연말 5일까지 이월 가능)

## 2. 특별 휴가

### 2.1 경조사 휴가
- 본인 결혼: 5일
- 자녀 결혼: 1일
- 배우자/본인 부모 사망: 5일
- 조부모/형제자매 사망: 3일

### 2.2 출산/육아 휴가
- 출산휴가: 90일(산전후휴가)
- 배우자 출산 휴가: 10일
- 육아휴직: 최대 1년 (만 8세 이하 자녀)
"""
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 20,
    separators=["\n##", "\n###", "\n\n", "\n", " "]
)

chunks = text_splitter.create_documents(documents)
print(f"총 {len(chunks)}개의 청크로 분할됨")
print(f"\n[청크1]\n{chunks[0].page_content[:200]}")