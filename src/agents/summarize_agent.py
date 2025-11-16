

import requests
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).parent.parent.parent  / 'config' / 'all_urls.yaml'

def load_all_urls_config():
    with CONFIG_PATH.open('r') as f:
        return yaml.safe_load(f)

url_config = load_all_urls_config()
summarize_output_url =url_config['summarize_output_url']


def summarize_output(state):
    try:
        query = state['query']
        search_results= state['data_for_summarize']
        res=requests.post(summarize_output_url,json={'query':query,"search_results": search_results})
        if res.status_code ==200:
            state['output']= res.json()
            state["summarize_output_status"] =True
            return state
        else:
            state["summarized_output_status"] =False
        return state
    except Exception as e:
        return state


