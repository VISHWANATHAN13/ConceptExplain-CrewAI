# import yaml
from agents.agents_config import load_yaml_file
from llm_config.load_llm import get_llm
from crewai import Agent, Task

agent_config = load_yaml_file("agents_configuration.yaml")
task_config = load_yaml_file("task_configuration.yaml")
llm = get_llm()
def create_content_retriever_agent():

    content_retriever_agent =  Agent(
        role = agent_config['content_retriever_agent']['role'],
        goal = agent_config['content_retriever_agent']['goal'],
        backstory = agent_config['content_retriever_agent']['backstory'],
        verbose = True,
        llm =llm
    )

    retriever_task = Task(
        description= task_config[
            "content_retrieval_task"
        ]["description"],
        expected_output = task_config[
            "content_retrieval_task"
        ]["expected_output"],
        agent=content_retriever_agent
    )
    return content_retriever_agent, retriever_task