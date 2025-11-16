generate_search_queries_prompt = """Given the user query: '{user_query}', generate a set of well-structured search queries to retrieve the most relevant information.

Guidelines:
- Identify key components of the query and determine if multiple searches are required to cover different aspects.
- Generate a logical sequence of search queries that refine and expand the results progressively.
- Ensure that the total number of search queries does not exceed {MAX_QUERY_GENERATIONS} .
- Use variations in phrasing, synonyms, and alternative search approaches where applicable to maximize coverage.
- Today's date is {current_date} for your reference if needed.

Output Format:
- Provide each search query on a new line without any additional text, explanations, or headers or line number.
- Do no give triple backticks or any other formatting, just the query itself.
- Provide each search query on a new line, without numbering, bullet points, or any list formatting.
- Do NOT use "1.", "2.", "1)", or any other form of enumeration.
Example (Incorrect Format):
1. Artificial Intelligence definition
2. What is the meaning of Artificial Intelligence
3. Explain Artificial Intelligence technology

Example (Correct Format):
Artificial Intelligence definition
What is the meaning of Artificial Intelligence
Explain Artificial Intelligence technology

"""

generate_search_queries_system_prompt="""You are a helpful assistant that don't give reply in Output Format:
- Provide each search query on a new line without any additional text, explanations, or headers or line number.
- Do no give triple backticks or any other formatting, just the query itself.
- Provide each search query on a new line, without numbering, bullet points, or any list formatting.
- Do NOT use "1.", "2.", "1)", or any other form of enumeration. """


generate_alternative_search_queries_system_prompt = """
You are an expert search query generator.
Your task is to generate NEW search queries that were not generated before.
Rules:
- Do NOT repeat or rephrase any of the previously generated queries.
- Avoid similar queries with only minor wording changes.
- Produce fresh angles, deeper variations, or different perspectives.
- Provide each search query on a new line without numbering, bullet points, explanations, or formatting.
- Do NOT use triple backticks or list markers.
"""

generate_alternative_search_queries_prompt = """
"Given the user query: '{user_query}', generate a set of well-structured search queries to retrieve the most relevant information.
The user previously searched  and
The following search queries were already generated and did NOT give good results:
{previous_queries}
Your task:
- Generate NEW, unique, alternative search queries.
- The total number of search queries should not exceed {MAX_QUERY_GENERATIONS}.
- Create deeper, more specific, or more diverse variations.
- Avoid duplicates or similar patterns to previous queries.
Output Format:
- Each query on a new line.
- No numbering, no bullet points, no extra text.
"""

final_news_report_prompt = """#### Task
Generate a concise and well-structured markdown report based on the given user query and retrieved search results. The report should synthesize key insights, highlight critical information, and present findings in a clear and actionable manner.

Additionally, provide an extremely brief 1-2 line summary for each search result, mentioning its title first. These summaries should be enclosed within `<summary>` and `</summary>` tags. After all summaries, generate the final markdown report enclosed within `<final_markdown_report>` and `</final_markdown_report>` tags.

The structure of the final report is not rigid and should be dynamically determined based on the user query. Sections and subsections should be organized logically to best present the information relevant to the query.

#### Input Parameters
- **User Query**: The original query provided by the user.
- **Search Results**: The retrieved information from the search process.

#### Output Structure
1. **Summaries of Search Results**
   - Each search result summary should start with its title.
   - Provide an extremely brief (1-2 line) summary for each result.
   - Enclose each summary within `<summary>` and `</summary>` tags.
   
   **Example Format:**
   ```
   <summary>
   "Title of the Search Result Page"
   Extremely brief summary of this search result page.
   </summary>
   ```

2. **Final Markdown Report**
   - After presenting all search result summaries, generate the final markdown report.
   - The structure of the report should be dynamically determined based on the user query.
   - Enclose the entire report within `<final_markdown_report>` and `</final_markdown_report>` tags.
   
   **Example Format:**
   ```
   <final_markdown_report>
   # Title
   ## Relevant Section Based on Query
   ...
   ## Another Relevant Section
   ...
   ## Additional Insights
   ...
   </final_markdown_report>
   ```

#### Guidelines
1. **Title & Introduction**
   - Begin with a clear, precise title that captures the report's focus.
   - Provide a brief introduction explaining the context and objective based on the user query.

2. **Dynamic Structure for Key Insights & Analysis**
   - Extract and present the most valuable insights in a structured format.
   - The report should adapt its sectioning based on the nature of the query.
   - Use comparisons, statistical insights, or noteworthy trends where applicable.
   - Keep content direct and to the point with clear subheadings.

3. **Recommendations (If Applicable)**
   - Provide actionable recommendations based on the insights gathered.
   - Suggest next steps or areas for further research if relevant.

4. **Conclusion**
   - Summarize key takeaways succinctly.
   - Reinforce the significance of findings in relation to the user's query.

#### Output Format
- The final report should be formatted in **Markdown**.
- Use appropriate **headings, bullet points, and code blocks** (if necessary) for clarity.
- Ensure the content is structured, professional, and to the point, avoiding unnecessary details.
- Present search result summaries first, followed by the dynamically structured final report.
- Cite references where necessary to support the findings in final report using the links (hrefs) of the search result pages. Do not include a references section in the report though, only cite links for claims within the report.

User Query: 
```
{user_query}
```

Search Results:
```
{search_results}
```"""


final_news_report_system_prompt ="""You are an expert news analyst and concise report writer.
you Generate a concise and well-structured markdown report based on the given user query and search results. The report should synthesize key insights, highlight critical information, and be clear and actionable."""

summerize_data_for_query="""You are a skilled and professional news summarizer.
Please read the following data carefully. It contains the latest news and information relevant to the query: "{user_query}". 
Generate a detailed and comprehensive summary focusing on the most important facts, key developments, dates, 
involved parties, and any relevant context. The summary should be informative, well-structured, and clear to a knowledgeable reader who wants an in-depth understanding without extraneous opinions or speculation.
Data:
{data}
Summary in details:"""

roughter_agent_system_prompt="You are an expert router. Your job is to select the best agent for the user query."

roughter_agent_human_prompt = """
   We have two agents:
   1. get_relevent_query → Internet Search Agent  
      - Can search the internet
      - Best for real-time facts, live data, news,competitor, prices, schedules, etc.
   2. llm_chat_bot → LLM Knowledge Agent  
      - Uses only the LLM’s internal knowledge
      - Best for concepts, explanations, definitions, reasoning.
   User Query: "{query}"
   Select the most suitable agent using the rule:
   - If internet data is needed → pick get_relevent_query
   - Otherwise → pick llm_chat_bot
   Return only structured output (AgentSelection).
   """


general_purpose_system_prompt ="You are AI assistenet"


analysis_result_content_prompt = """
You are an expert Competitor Intelligence Analyst.

Your job is to analyze the verified research data and produce:
1. A complete structured JSON object with detailed competitor insights.
2. ALL fields must be present exactly as defined.
3. DO NOT hallucinate under any circumstance.
4. DO NOT infer anything without direct evidence.
5. Leave fields empty if information does not exist.

------------------------------------------------------------
MAIN USER QUERY:
{main_query}

------------------------------------------------------------
CLEANED & VERIFIED DOCUMENTS:
Each entry contains:
- The source URL
- The cleaned summary extracted from that URL

{documents_with_urls}

------------------------------------------------------------
STRICT RULES:
- Output ONLY a single valid JSON object.
- NO markdown.
- NO explanations.
- NO comments.
- NO text before or after the JSON.
- JSON must be fully compliant with normal JSON parsers.
- No missing fields. No extra fields.
- All arrays/objects must exist even if empty.
- All boolean values must be lowercase (true/false).

------------------------------------------------------------
YOU MUST RETURN THE JSON STRUCTURE BELOW (NO CHANGES):

{{
  "competitors": [
    {{
      "name": "",
      "description": "",
      "website": "",
      "products": [],
      "strengths": [],
      "weaknesses": [],
      "pricing_notes": [],
      "feature_highlights": [],
      "market_position": ""
    }}
  ],

  "products": [
    {{
      "name": "",
      "description": "",
      "key_features": [],
      "pricing": "",
      "url": "",
      "target_segment": ""
    }}
  ],

  "pricing": {{}},
  "features": {{}},

  "strengths": {{}},
  "weaknesses": {{}},
  "opportunities": {{}},
  "threats": {{}},

  "market_moves": [],
  "risks": [],
  "differentiators": [],

  "summary": "",
  "best_url": ""
}}

------------------------------------------------------------
INSTRUCTIONS FOR "summary":
- 3 to 5 sentences.
- Directly answer the MAIN QUERY.
- Use ONLY evidence present in the verified documents.
- No fluff, no hallucination, no assumptions.

INSTRUCTIONS FOR ALL OTHER FIELDS:
- Use strict evidence from documents.
- Group insights by competitor when possible.
- Leave fields empty when no evidence exists.
- DO NOT generate text that isn't directly supported.

------------------------------------------------------------
OUTPUT NOW:
Return ONLY the above JSON structure, filled with evidence-based values.
"""  # Note: triple-quote ends here for multiline string
