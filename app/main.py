from fastapi import FastAPI

from api import relevant_queries
from api import search_duckduckgo
from api import web_data_fetcher
from api import summarize_news_data
from api import store_data_in_vector_db
from api import search_data_in_vector_db
from api import analysis_search_result
from api import concatenated_search


app = FastAPI()

app.include_router(relevant_queries.router, prefix="/api", tags=["Relevant Queries"])
app.include_router(concatenated_search.router, prefix="/api", tags=["Concatenated Search"])
app.include_router(search_duckduckgo.router, prefix="/api", tags=["Search News"])
app.include_router(web_data_fetcher.router, prefix="/api", tags=["Fetch data from web"])
app.include_router(store_data_in_vector_db.router, prefix="/api", tags=["Store data In DB "])
app.include_router(search_data_in_vector_db.router, prefix="/api", tags=["search data In DB "])
app.include_router(summarize_news_data.router, prefix="/api", tags=["Summarize News Data "])
app.include_router(analysis_search_result.router, prefix="/api", tags=["Analysis content "])


