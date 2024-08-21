from llama_index.agent.openai import OpenAIAgent

from .prompts import REPORT_WRITER_PROMPT


def create_report_writer_agent(llm):
    """ 
    Agent responsible for writing the draft of report based on the present context.
    """
    agent = OpenAIAgent.from_tools(llm=llm, system_prompt=REPORT_WRITER_PROMPT, 
                                   verbose=True)
    return agent 