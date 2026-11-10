from collections.abc import Iterator

from langchain.chat_models import BaseChatModel, init_chat_model
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import BaseMessage

from my_agent.config import get_settings


def createModel(modelName: str | None = None) -> BaseChatModel:
    settings = get_settings()
    model_name = modelName or settings.default_model

    if not settings.openai_api_key:
        raise ValueError("OPEN API KEY NOT FOUND")

    return init_chat_model(model_provider="openai",
                           model=model_name,
                           api_key = settings.openai_api_key.get_secret_value()
                           )

DEFAULT_SYSTEM_PROMPT = """
너는 친절한 AI 어시스턴트. 사용자의 질문에 명확하고 간결하게 답변. 추측하지 말고 답변할것.
"""

class Agent:
    def __init__(self, model: BaseChatModel | None = None, system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.model = model if model is not None else createModel()
        self.system_prompt = system_prompt
        self.messages: list[BaseMessage] = [
            SystemMessage(content=self.system_prompt)
        ]

    def chat(self, user_message: str) -> str:
        self.messages.append(HumanMessage(content=user_message))
        response = self.model.invoke(self.messages)
        self.messages.append(response)
        return response.text

    def stream(self, user_message: str) -> Iterator[str]:
        self.messages.append(HumanMessage(content=user_message))
        full_response = ""

        for chunk in self.model.stream(self.messages):
            if chunk.text:
                full_response += chunk.text
                yield chunk.text
        self.messages.append(AIMessage(content=full_response))

    def clear_history(self) -> None:
        self.messages = [SystemMessage(content=self.system_prompt)]

def create_agent(model_name: str | None = None, system_prompt: str | None = None) -> Agent:
    model = createModel(modelName=model_name)
    return Agent(model=model, system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT)
