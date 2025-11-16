from typing import TypedDict,Literal,Annotated,List, Any, Optional
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: List[BaseMessage]
    query:str
    router: Literal["llm_chat_bot","get_relevent_query"] 
    relevent_query: Optional[List[str]]
    relevent_query_operation_status: Literal[True,False] =False
    search_duckduck_go: Optional[str]
    search_duckduck_go_status: Literal[True,False] =False
    data_for_summarize:Optional[Any]
    web_urls:List[str]
    web_data_fetch_status: Literal[True,False] =False
    summarized_output: Any
    get_summarize_query: Optional[str]
    summarize_output_status:Literal[True,False] =False
    output: Optional[str] = 'Failed to fetch respomnse'

