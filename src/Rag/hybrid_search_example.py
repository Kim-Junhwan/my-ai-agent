from unittest import result

from langchain_openai import OpenAIEmbeddings
from opensearchpy import OpenSearch

from my_agent.config import get_settings

settings = get_settings()

client = OpenSearch(hosts=[{"host": settings.opensearch_host, "port": settings.opensearch_port}])
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)

def hybrid_search(
        query: str,
        index_name: str,
        k: int,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3
) -> list[dict]:
    query_vector = embeddings.embed_query(query)

    search_query = {
        "size": k,
        "query": {
            "hybrid": {
                "queries": [
                    {
                        "knn": {
                            "embedding" : {
                                "vector": query_vector,
                                "k": k * 2,
                            }
                        }
                    },

                    {
                        "match": {
                            "content": {
                                "query": query,
                                "boost": 1.0
                            }
                        }
                    }
                ]
            }
        },
        "search_pipeline": {
            "phase_results_processors": [
                {
                    "normalization-processor": {
                        "normalization": {"technique": "min_max"},
                        "combination": {
                            "technique": "arithmetic_mean",
                            "parameters": {
                                "weights": [vector_weight, keyword_weight]
                            }
                        }
                    }
                }
            ]
        }
    }

    response = client.search(index=index_name, body=search_query)

    results = []
    for hit in response["hits"]["hits"]:
        results.append({
            "_id": hit["_id"],  # 인덱싱할 때 지정한 문서 ID ("0", "1", ...)
            "content": hit["_source"]["content"],
            "score": hit["_score"],
            "metadata": hit["_source"].get("metadata", {}),
        })

    return results

def evaluate_search_quality(
        test_quieries: list[dict],
        vector_weight: float,
        keyword_weight: float,
) -> float:
    total_score = 0
    for test in test_quieries:
        results = hybrid_search(
            query=test["query"],
            index_name="company_docs",
            k = 5,
            vector_weight=vector_weight,
            keyword_weight=keyword_weight,
        )

        relevant_count = sum(
            1 for r in results
            if r.get("_id") in test["relevant_doc_ids"]
        )

        precision = relevant_count / len(results)
        total_score += precision

    return total_score / len(test_quieries)

test_data = [
    {"query": "errorCode E-1001", "relevant_doc_ids":["12"]},       # 6.1 신청 단계 오류
    {"query": "휴가 신청하고 싶어요.", "relevant_doc_ids":["1", "8"]}  # 1.2 사용 방법, 4.1 신청
]

# 정답 ID(relevant_doc_ids)를 정하기 위해 질문별 검색 결과를 먼저 확인
for test in test_data:
    print(f"\n[질문] {test['query']}")
    for r in hybrid_search(query=test["query"], index_name="company_docs", k=5):
        preview = r["content"][:60].replace("\n", " ")
        print(f"  _id={r['_id']}  score={r['score']:.3f}  {preview}")
print()

weight_combinations = [
    (0.5, 0.5),
    (0.7, 0.3),
    (0.3, 0.7),
    (0.8, 0.2)
]

for vec_w, key_w in weight_combinations:
    score = evaluate_search_quality(test_data, vec_w, key_w)
    print(f"벡터 {vec_w}, 키워드: {key_w} -> MAP: {score: .3f}")