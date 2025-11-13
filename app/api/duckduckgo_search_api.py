from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import sys

# Add src/utils and src/prompt_engineering to sys.path for imports
utils_path = Path.cwd().parent / "src" / "utils"
if str(utils_path) not in sys.path:
    sys.path.insert(0, str(utils_path))

prompt_path = Path.cwd().parent / "src" / "prompt_engineering"
if str(prompt_path) not in sys.path:
    sys.path.insert(0, str(prompt_path))

from huggin_face_client import ConnectHugginface
from duckduckgo_search import DuckDuckGo
from prompt_template import generate_search_queries_prompt
from lite_llm_client import create_chat_model


router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.post("/search/news", tags=["search"], summary="News search with publish date")
async def search_news(request: SearchRequest = Body(...)):
    try:
        print(request)
        search_results  = []
        duck_obj = DuckDuckGo()
        search_results.append(duck_obj.get_all_data_about(request.query, search_results ))
        return search_results 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")