from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal,Annotated,List
from langchain_core.messages import HumanMessage,SystemMessage
from pathlib import Path
import sys

src_path = Path.cwd().parent / 'llm'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

prompt_path = Path.cwd().parent /  "prompt_engineering"
if str(prompt_path) not in sys.path:
    sys.path.insert(0, str(prompt_path))

from prompt_template import general_purpose_system_prompt
from lite_llm_client import create_chat_model


def llm_chat_bot(state):
    try:
        user_query= state['query']
        system_msg = SystemMessage(content=general_purpose_system_prompt)
        human_msg = HumanMessage(content=user_query)
        connection_status = create_chat_model()

        if not connection_status.get('status'):
            state['output'] = "Unable to perfrom operation" +  + str(connection_status.text) +' kk'
        llm =connection_status['model']
        response = llm.invoke([system_msg, human_msg]).content
        state['output']= response 
        return state
    except Exception as e:
        state['output'] = "Unable to perfrom operation" + str(e)
        return state