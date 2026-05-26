# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 개발자 컨텍스트

- 2년차 iOS 개발자 (Swift/Xcode 경험 보유, Python 경험 없음)
- 이 프로젝트는 **"LangGraph로 만드는 AI 에이전트 서비스"** 책의 예제를 따라하며 LangGraph를 학습하는 것이 목적
- Python 문법, 패키지 생태계, 관행이 낯설 수 있으므로 설명 시 iOS/Swift 개념과 비교하거나 배경 설명을 충분히 제공할 것
- 책 예제 코드를 그대로 따라가는 상황이므로 불필요한 구조 변경이나 과도한 리팩토링 제안은 자제할 것

## Package Manager

이 프로젝트는 **uv**를 사용한다. `pip` 대신 아래 명령어를 사용할 것.

```bash
# 의존성 설치
uv sync

# 패키지 추가
uv add <package>

# 가상환경 내 명령 실행
uv run <command>
```

## 실행 방법

```bash
# Streamlit 앱 실행
uv run streamlit run src/app.py
```

## 환경 변수

`.env.example`을 복사해 `.env`를 만들고 값을 채워야 한다.

```
OPENAI_API_KEY=...
DEFAULT_MODEL=...   # 기본값: gpt-5.2
DEBUG=false
```

설정은 `src/my_agent/config.py`의 `Settings` 클래스(pydantic-settings)가 `.env`에서 자동으로 로드한다.

## 아키텍처

```
src/
  app.py                  # Streamlit 진입점
  my_agent/
    config.py             # pydantic-settings 기반 환경 설정 (Settings, get_settings)
    agent.py              # 에이전트 로직
    __init__.py
```

- **설정**: `get_settings()`를 호출하면 `.env`를 읽어 `Settings` 인스턴스를 반환한다. API 키는 `SecretStr` 타입.
- **LLM**: langchain-openai / langchain-anthropic / langchain-google-genai 모두 의존성에 포함되어 있어 멀티 프로바이더 사용이 가능하다.
- **워크플로우 오케스트레이션**: langgraph가 설치되어 있다.

## IDE Python 인터프리터 설정

`pydantic_settings` 등 패키지를 IDE가 인식하지 못하면 인터프리터를 `.venv`로 지정해야 한다.

- VS Code: `Python: Select Interpreter` → `./.venv/bin/python` 선택
- 가상환경 경로: `.venv/` (uv가 프로젝트 루트에 생성)
