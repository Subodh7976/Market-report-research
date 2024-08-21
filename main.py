from llama_index.llms.openai import OpenAI
from llama_index.core.tools.query_engine import QueryEngineTool
from llama_index.agent.openai import OpenAIAgent

from agents import (
    create_context_retriever_agent,
    create_report_writer_agent,
    create_reviewer_agent
)
from utils import create_pdf
from logger import setup_logging

from dotenv import load_dotenv
load_dotenv()


def create_agent():
    llm = OpenAI(model="gpt-4o-mini", temperature=0.1)

    context_retriever_tool = QueryEngineTool.from_defaults(
        create_context_retriever_agent(llm),
        name="context_retriever",
        description="""
        Agent responsible for building the context relevant to the query by performing 
        web search and scraping.
        Requires description of the problem for which context is needed.
        """
    )

    report_writer_tool = QueryEngineTool.from_defaults(
        create_report_writer_agent(llm),
        name="report_writer",
        description="""
        Agent responsible for writing the draft of report based on the provided context.
        Requires context as input and research topic.
        """
    )

    reviewer_tool = QueryEngineTool.from_defaults(
        create_reviewer_agent(llm),
        name="reviewer",
        description=""" 
        Agent responsible for reviewing the report and providing feedback on how to improve it
        """
    )

    orchestrating_agent = OpenAIAgent.from_tools(
        [context_retriever_tool, report_writer_tool, reviewer_tool],
        llm=llm,
        system_prompt="""
        Manages the workflow and coordination among all agents. Assigns tasks, sets deadlines, and ensures smooth communication and integration of information. 
        Responsible for overseeing the entire project to ensure timely and accurate completion.
        
        Generate the final detailed report for the user query along with citations.
        
        Given will be the company information, Research Topic (the new feature which needs to be researched with respect to existing features or competitors) and 
        competitors (competitors list which will be researched for the new proposed feature). Keep your research fair and based on the context only, 
        do not try to favor any single company.
        """,
        verbose=True
    )

    return orchestrating_agent


if __name__ == "__main__":
    logger = setup_logging()
    logger.info("The logging has started!!!")
    agent = create_agent()
    query = """ 
    Company information - Produx.ai is a software company that provides a product management platform designed to help businesses manage their product development processes more efficiently. The platform offers tools for customer discovery, feature prioritization, PRD generation, etc., feature prioritization, and stakeholder communication. It aims to streamline the workflow of product teams by integrating with other tools and providing data-driven insights to enhance decision-making and collaboration.
    
    Compare Produx with www.preskale.com/
    """
    response = agent.query(query)
    print(response)
    create_pdf(str(response))
