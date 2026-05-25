import streamlit as st
import time

st.set_page_config(page_title="AI Agent Chat", page_icon="🤖")
st.title("🤖 AI Agent Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def stream_response(text: str):
    for char in text:
        yield char
        time.sleep(0.02)

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({ "role":"user" , "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response_text = f"안녕하세요! '{prompt}'에 대해 답변드리겠습니다."
    with st.chat_message("assistant"):
        response = st.write_stream(stream_response(response_text))

    st.session_state.messages.append({"role":"assistant", "content":response})