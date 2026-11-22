
from httpx import delete
from langchain_openai import OpenAIEmbeddings
from numpy import indices
from opensearchpy import OpenSearch

from my_agent.config import get_settings
from Rag.rag_example import chunks


settings = get_settings()

client = OpenSearch(
    hosts=[{"host": settings.opensearch_host, "port": settings.opensearch_port}],
    http_auth=None,
    use_ssl=False
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)
index_name = "company_docs"

index_body = {
    "settings" : {
        "index": {
            "knn": True,
        }
    },
    "mappings": {
        "properties": {
            "content": {"type":"text"},
            "embedding": {
                "type": "knn_vector",
                "dimension": 1536,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "nmslib",
                }
            },
            "metadata": {"type": "object"},
        }
    }
}

if client.indices.exists(index=index_name):
    client.indices.delete(index=index_name)
client.indices.create(index=index_name, body=index_body)

print(f"인덱스 '{index_name}' 생성 완료")

for i, chunk in enumerate(chunks):
    vector = embeddings.embed_query(chunk.page_content)

    doc = {
        "content": chunk.page_content,
        "embedding": vector,
        "metadata": {
            "source":"휴가정책.md",
            "chunk_index": i
        }
    }
    client.index(index=index_name, body=doc, id=str(i))

client.indices.refresh(index=index_name)

print(f"{len(chunks)}개 문서 인덱싱 완료")

def search_document(query: str, k: int = 3) -> list[dict]:
    query_vector = embeddings.embed_query(query)
    search_query = {
        "size": k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": k,
                }
            }
        }
    }

    response = client.search(index=index_name, body=search_query)

    results = []

    for hit in response["hits"]["hits"]:
        results.append({
            "content": hit["_source"]["content"],
            "score": hit["_score"],
            "metadata": hit["_source"]["metadata"],
        })
    return results