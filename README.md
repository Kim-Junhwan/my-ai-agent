# My AI Agent

『LangGraph로 만드는 AI 에이전트 서비스』의 예제를 따라 파이썬과 AI 에이전트 개발을 학습하는 프로젝트입니다. 현재는 LangChain으로 OpenAI 모델을 호출하고, Streamlit으로 대화형 챗봇 화면을 제공합니다.

## 주요 기능

- AI 응답을 실시간으로 표시하는 스트리밍 채팅
- 현재 세션의 대화 기록을 활용한 연속 대화
- 사이드바에서 시스템 프롬프트 변경 및 대화 초기화

## 실행 방법

Python 3.13 이상과 [uv](https://docs.astral.sh/uv/)가 필요합니다. 아래 명령은 모두 프로젝트 루트에서 실행합니다.

### 1. 의존성 설치

```bash
uv sync
```

### 2. 환경 변수 설정

`.env` 파일이 없다면 예제 파일을 복사합니다. 이미 있다면 기존 파일을 수정하세요.

```bash
cp .env.example .env
```

`.env`의 예시 값을 실제 설정으로 바꿉니다.

```dotenv
OPENAI_API_KEY=본인의_API_키
DEFAULT_MODEL=gpt-5.2
DEBUG=false
```

현재 챗봇 화면은 `gpt-5.2`를 선택해 사용합니다. `DEFAULT_MODEL`은 코드에서 모델 이름을 지정하지 않을 때 적용되는 기본값입니다. `.env`는 Git 추적에서 제외됩니다.

### 3. 챗봇 실행

```bash
uv run streamlit run src/app.py
```

실행 후 터미널에 표시되는 Local URL(기본 `http://localhost:8501`)을 브라우저에서 엽니다. 하단 입력창에 메시지를 입력하면 대화를 시작할 수 있습니다.

시스템 프롬프트를 변경하면 기존 대화가 초기화됩니다. 실행을 종료하려면 터미널에서 `Ctrl+C`를 누르세요.

## 프로젝트 구조

```text
src/
├── app.py                # Streamlit 화면 및 사용자 입력 처리
└── my_agent/
    ├── __init__.py
    ├── agent.py          # 모델 생성, 대화 기록 및 응답 스트리밍
    └── config.py         # .env 기반 환경 설정
```
