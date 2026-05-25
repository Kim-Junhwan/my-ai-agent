import streamlit as st

st.set_page_config(
    page_title= "AI Agent Chat",
    page_icon="🤖",
    layout= "centered"
)

st.title("🤖 AI Agent Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메세지를 입력하세요"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = f"입력하신 메시지: {prompt}"
    st.session_state.messages.append({"role":"assistant", "content":response})
    with st.chat_message("assistant"):
        st.markdown(response)