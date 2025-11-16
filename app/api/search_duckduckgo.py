from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import sys

# Add src/utils and src/prompt_engineering to sys.path for imports
utils_path = Path.cwd().parent / "src" / "utils"
if str(utils_path) not in sys.path:
    sys.path.insert(0, str(utils_path))

from duckduckgo_search import DuckDuckGo

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    max_url: int =3

@router.post("/search/duckduckgo", tags=["search"], summary="News search with publish date")
async def search_news(request: SearchRequest = Body(...)):
    try:
        duck_obj = DuckDuckGo()
        search_results=duck_obj.search_duckduckgo(request.query )
        return search_results 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")