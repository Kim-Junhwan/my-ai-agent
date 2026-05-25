from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([("system","당신은 친절한 AI 어시스턴트입니다."),("user","{input}")])

messages = prompt.invoke({"input":"안녕하세요"})
print("생성된 프롬프트:")
for msg in messages.messages:
    print(f" [{msg.type}] {msg.text}")