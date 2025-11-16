from langgraph.graph import StateGraph,START,END
from state import State
from pathlib import Path
import sys


def get_router(state):
    router_output= state['router']
    print(state)
    return router_output

agent_path = Path.cwd().parent / "src" / "agents"
print('mmmmmmmmmmmmmmmm',agent_path)
if str(agent_path) not in sys.path:
    sys.path.insert(0, str(agent_path))

from routeragent import router
from llm_chat_bot_agent import llm_chat_bot
from search_duckduck_go_agent_1 import search_over_intenet_with_ddg as d1
from search_duckduck_go_agent_2 import search_over_intenet_with_ddg as d2
from search_duckduck_go_agent_3 import search_over_intenet_with_ddg as d3
from web_data_fetch import web_data_fetch
from summarize_agent import summarize_output
from get_relevent_query import get_relevent_query




graph = StateGraph(State)
graph.add_node("router",router)
graph.add_node("llm_chat_bot",llm_chat_bot)
graph.add_node("get_relevent_query",get_relevent_query)
graph.add_node("search_1",d1)
graph.add_node("search_2",d2)
graph.add_node("search_3",d3)
graph.add_node("web_data_fetch",web_data_fetch)
graph.add_node("summarize_output",summarize_output)


graph.add_edge(START,'router')
graph.add_conditional_edges('router',get_router,{"llm_chat_bot":"llm_chat_bot","get_relevent_query":"get_relevent_query"})
graph.add_edge("get_relevent_query","search_1")
graph.add_edge("get_relevent_query","search_2")
graph.add_edge("get_relevent_query","search_3")
graph.add_edge("search_1","web_data_fetch")
graph.add_edge("search_2","web_data_fetch")
graph.add_edge("search_3","web_data_fetch")
graph.add_edge("web_data_fetch","summarize_output")
graph.add_edge("summarize_output",END)
graph.add_edge("llm_chat_bot",END)
compiled= graph.compile()

compiled.invoke({'query':'hi'})


