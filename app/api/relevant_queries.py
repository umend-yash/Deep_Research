from fastapi import APIRouter, Body, HTTPException
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
from pathlib import Path
import sys


utils_path = Path.cwd().parent / "src" / "utils"
if str(utils_path) not in sys.path:
    sys.path.insert(0, str(utils_path))

prompt_path = Path.cwd().parent / "src" / "prompt_engineering"
if str(prompt_path) not in sys.path:
    sys.path.insert(0, str(prompt_path))

from huggin_face_client import ConnectHugginface
from duckduckgo_search import DuckDuckGo
from prompt_template import generate_search_queries_prompt,generate_search_queries_system_prompt

router = APIRouter()

@router.post("/search/relevant-queries", tags=["search"],summary="Generate relevant search queries",description="Generates relevant search queries based on user input using Huggingface LLM.")
async def generate_relevant_queries( query: str = Body(..., description="User query string"),
    max_query_generation: int = Body(3, description="Maximum number of queries to generate")):
    """
    Takes user query and returns a list of refined search queries.
    """
    current_date = datetime.today().strftime("%d %B %Y")
    connection_status = ConnectHugginface()

    if not connection_status.get('status'):
        raise HTTPException(status_code=503, detail="Unable to connect to Huggingface model")

    llm = connection_status['model']

    system_msg = SystemMessage(content=generate_search_queries_system_prompt)
    human_msg = HumanMessage(content=generate_search_queries_prompt.format(
            user_query=query,
            current_date=current_date,
            MAX_QUERY_GENERATIONS=max_query_generation,
        ))
    response=llm.invoke([system_msg, human_msg])

    refined_queries = [
        q.strip().strip("'\"").strip("-").strip()
        for q in response.content.split("\n")
        if q and q.lower() != "none"
    ]
    refined_search_queries = refined_queries[:max_query_generation]
    return {"queries_generated": refined_search_queries}
