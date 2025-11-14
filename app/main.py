from fastapi import FastAPI

from api import duckduckgo_search_api
from api import relevant_queries
from api import summarize_news_data
from api import store_data_in_vector_db
from api import search_data_in_vector_db

app = FastAPI()

app.include_router(relevant_queries.router, prefix="/api", tags=["Relevant Queries"])
app.include_router(duckduckgo_search_api.router, prefix="/api", tags=["Search News"])
app.include_router(summarize_news_data.router, prefix="/api", tags=["Summarize News Data "])
app.include_router(store_data_in_vector_db.router, prefix="/api", tags=["Store data In DB "])
app.include_router(search_data_in_vector_db.router, prefix="/api", tags=["search data In DB "])


