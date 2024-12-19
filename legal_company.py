import os
from lightrag import LightRAG, QueryParam
import logging
import numpy as np
from lightrag.llm import openai_complete_if_cache
from lightrag.llm import openai_embedding
from lightrag.base import EmbeddingFunc

from markdown_parser import MarkdownParser

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("lightrag").setLevel(logging.DEBUG)

GLM_API_KEY = "xxx"
DEEPSEEK_API_KEY = "xxx"
MODEL = "deepseek-chat"

WORKING_DIR = "./md6_2048"

async def deepseepk_model(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        MODEL,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1",
        **kwargs
    )

def remove_if_exist(file):
    if os.path.exists(file):
        os.remove(file)

async def GLM_embedding(texts: list[str]) -> np.ndarray:
    return await openai_embedding(
        texts,
        model="embedding-3",
        api_key=GLM_API_KEY,
        base_url="https://open.bigmodel.cn/api/paas/v4"
    )

def init():
    from time import time

    with open("./legal/company.md", encoding="utf-8-sig") as f:
        TEXT = f.read()

    # remove_if_exist(f"{WORKING_DIR}/vdb_entities.json")
    # remove_if_exist(f"{WORKING_DIR}/kv_store_full_docs.json")
    # remove_if_exist(f"{WORKING_DIR}/kv_store_text_chunks.json")
    # remove_if_exist(f"{WORKING_DIR}/kv_store_community_reports.json")
    # remove_if_exist(f"{WORKING_DIR}/graph_chunk_entity_relation.graphml")

    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=deepseepk_model,
        embedding_func=EmbeddingFunc(
            embedding_dim=2048,
            max_token_size=2048,
            func=GLM_embedding
        ),
        llm_model_max_async=40,
        embedding_func_max_async=1,
        markdown_chunk_parser=MarkdownParser,
    )
    start = time()
    rag.insert(TEXT)
    print("indexing time:", time() - start)


if __name__ == "__main__":
    # init()
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=deepseepk_model,
        embedding_func=EmbeddingFunc(
            embedding_dim=2048,
            max_token_size=2048,
            func=GLM_embedding
        ),
        llm_model_max_async=1,
        embedding_func_max_async=1,
    )
    # Perform hybrid search
    print(rag.query("请问第十章每一条讲什么？", param=QueryParam(mode="hybrid")))