from llama_index.agent.openai import OpenAIAgent

from .prompts import REVIEWER_PROMPT 


def create_reviewer_agent(llm):
    """ 
    Agent responsible for reviewing the report and providing feedback on how to improve it
    """
    agent = OpenAIAgent.from_tools(llm=llm, system_prompt=REVIEWER_PROMPT, 
                                   verbose=True)
    return agent 
