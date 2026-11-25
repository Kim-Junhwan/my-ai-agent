from langchain_openai import OpenAIEmbeddings

from my_agent.config import get_settings

settings = get_settings()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)

text1 = "고양이는 부드럽다."
text2 = "부드러운걸 만지면 기분이 좋다."
text3 = "비행기를 타러 3번 게이트에 갑니다."

vec1 = embeddings.embed_query(text1)
vec2 = embeddings.embed_query(text2)
vec3 = embeddings.embed_query(text3)

print(f"차원: {len(vec1)}")
print(f"예시 (처음 5개)): {vec1[:5]}")