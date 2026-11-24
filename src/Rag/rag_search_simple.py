from pydoc import doc

from langchain.chat_models import init_chat_model
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_core import retrievers
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from openai import api_key, vector_stores

from my_agent.config import get_settings

settings = get_settings()

vector_stores = OpenSearchVectorSearch(
    opensearch_url= f"{settings.opensearch_host}:{settings.opensearch_port}",
    index_name="company_docs",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key),
)

retrievers = vector_stores.as_retriever(
    search_type="similarity",
    search_kwargs={"k":3, "text_field": "content", "vector_field": "embedding"}
)

prompt = ChatPromptTemplate.from_template("""
주어진 문서만을 참고하여 질문에 답변하시오.

규칙: 

1. 문서에 있는 내용만 답변하세요.

2. 문서에 없는 내용은 "해당 정보는 문서에서 확인할 수 없습니다." 라고 답변하세요.

3. 답변 끝에 참고한 문서 출처를 명시하세요.

[참고 문서]
{context}

[질문]
{question}
""")

llm = init_chat_model(
    model_provider="openai",
    model="gpt-5.2",
    temperature=0,
    api_key=settings.openai_api_key
)

def format_docs(docs):
    return "\n\n--\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retrievers | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("육아휴직 기간은 얼마나 되나요?")
print(f"답변: {answer}")