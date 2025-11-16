from fastapi import APIRouter, Body, HTTPException
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime
from pathlib import Path
import sys

utils_path = Path.cwd().parent / "src" / "utils"
if str(utils_path) not in sys.path:
    sys.path.insert(0, str(utils_path))

from zilliz_vectorstore import search_in_vector_store

router = APIRouter()

class QueriesList(BaseModel):
    queries: List[str]

@router.post("/search/concatenated_search", tags=["LLM Search"], summary="Concatenate queries and search")
async def concatenated_search(payload: QueriesList):
    try:
        queries = payload.queries
        # Concatenate queries into single string
        concatenated_query = " ".join(queries)

        # Call your existing async search function using concatenated query string
        search_results = await search_in_vector_store(concatenated_query, top_k=5)

        return {
            "queries_received": queries,
            "concatenated_query": concatenated_query,
            "search_results": search_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in concatenated search: {e}")
