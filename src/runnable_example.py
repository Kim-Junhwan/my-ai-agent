from typing import final
from unittest import result

from langchain.chat_models import BaseChatModel, init_chat_model
from langchain.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from my_agent import get_settings


model = init_chat_model(model_provider="openai", model="gpt-5.2", api_key = get_settings().openai_api_key.get_secret_value())
prompt = ChatPromptTemplate.from_messages([
    ("human","{question}에 대해 설명해주세요. 한줄이내로."),
    ("system","사용자의 대답에 영어로만 답해주세요.")
    ])
parser = StrOutputParser()

def preProcess(text: str) -> dict:
    return {"question": text.strip().lower()}

def postProcess(message: BaseChatModel) -> str:
    return message.text.upper()

preprocess_runnable=RunnableLambda(preProcess)
postprocess_runnable=RunnableLambda(postProcess)

chain = preprocess_runnable | prompt | model | postprocess_runnable
result = chain.invoke("cat")
print(result)