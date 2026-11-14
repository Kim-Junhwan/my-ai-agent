from typing import final
from unittest import result

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from my_agent import get_settings


model = init_chat_model(model_provider="openai", model="gpt-5.2", api_key = get_settings().openai_api_key.get_secret_value())
prompt = ChatPromptTemplate.from_template("{topic}에 대해 설명해주세요. 간단하게 10줄 이내로.")
parser = StrOutputParser()

prompt_value = prompt.invoke({"topic":"양자컴퓨팅"})
print(prompt_value)
model_output = model.invoke(prompt_value)
print(model_output)
final_result = parser.invoke(model_output)
print(final_result)

print("----------------")

chain = prompt | model | parser
result = chain.invoke({"topic":"양자컴퓨팅"})
print(result)