from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent

from skills import google_search_scrape
from .prompts import CONTEXT_RETRIEVER_PROMPT


def create_context_retriever_agent(llm):
    """ 
    Agent responsible for building the context relevant to the query.
    """
    tools = [
        FunctionTool.from_defaults(google_search_scrape)
    ]

    agent = OpenAIAgent.from_tools(tools=tools, llm=llm, system_prompt=CONTEXT_RETRIEVER_PROMPT,
                                   verbose=True)

    return agent
