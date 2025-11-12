from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import SystemMessage, HumanMessage
from huggin_face_client import ConnectHugginface
import requests
import bs4

from pathlib import Path
import sys
prompt_path = Path.cwd().parent / "src" / "prompt_engineering"
if str(prompt_path) not in sys.path:
    sys.path.insert(0, str(prompt_path))

from prompt_template import summerize_data_for_query

class DuckDuckGo:
    def __init__(self, max_results=3):
        self.wrapper = DuckDuckGoSearchAPIWrapper(max_results=max_results)

    def search_duckduckgo(self, query):
        results = self.wrapper.results(query, max_results=self.wrapper.max_results)
        return results


    def fetch_url_text(self, url,user_query):
        try:
            if str(url).startswith('https:'):
                res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                soup = bs4.BeautifulSoup(res.text, "lxml")
                text_content = soup.body.get_text(" ", strip=True) if soup.body else ""
                connection_status = ConnectHugginface()

                if not connection_status.get('status'):
                    print('why here')
                    return text_content[:5000]
                system_msg = SystemMessage(content="You are a helpful assistant specializing in news summarization.")
                human_msg = HumanMessage(content=summerize_data_for_query.format(user_query=user_query,data=text_content[:20000]))
                llm =connection_status['model']
                output=llm.invoke([system_msg, human_msg])
                return output.content
            else:
                return  None
        except Exception as e:
            print('eeeeeeeeeeeeee',e)
            return None
        
    def get_all_data_about(self,query,have_data):
        try:
            output={}
            response=self.search_duckduckgo(query)
            for content in response:
                url=content['link']
                if url not in have_data:
                    output[url]=self.fetch_url_text(url,query)
                else:
                    continue
            return output
        except Exception as e:
            print('get all data error ',e)
            return output
    
