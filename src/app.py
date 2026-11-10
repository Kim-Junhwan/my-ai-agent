import streamlit as st

from my_agent.agent import create_agent

st.set_page_config(
    page_title="My AI Agent",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("설정")

    model_options=["gpt-5.2"]
    model_name=st.selectbox("모델", options=model_options, index=0)

    custom_prompt = st.text_area(
       label="시스템 프롬프트",
       value="",
       height=100
   )

    st.divider()

    if st.button(label="대화 초기화", use_container_width=True):
        st.session_state.messages = []
        if "agent" in st.session_state:
            st.session_state.agent.clear_history()
        st.rerun()

st.title("My Ai Agent")
agent_key=f"{model_name}_{hash(custom_prompt)}"

if "agent_key" not in st.session_state or st.session_state.agent_key != agent_key:
    try:
        st.session_state.agent = create_agent(
            model_name=model_name,
            system_prompt=custom_prompt if custom_prompt else None,
        )
        st.session_state.agent_key = agent_key
        st.session_state.messages = []
    except ValueError as e:
        st.error(f"[오류] 에이전트 초기화 실패: {e}")
        st.info("💡 .env 파일에 API 키가 설정되어 있는지 확인하세요.")
        st.stop()

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성(스트리밍)
    with st.chat_message("assistant"):
        response = st.write_stream(st.session_state.agent.stream(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})
