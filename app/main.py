from fastapi import FastAPI

from api import duckduckgo_search_api
from api import relevant_queries
from api import summarize_news_data

app = FastAPI()

app.include_router(relevant_queries.router, prefix="/api", tags=["Relevant Queries"])
app.include_router(duckduckgo_search_api.router, prefix="/api", tags=["Search News"])
app.include_router(summarize_news_data.router, prefix="/api", tags=["Summarize News Data "])



