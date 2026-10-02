# import yaml
from agents.agents_config import load_yaml_file
from llm_config.load_llm import get_llm
from crewai import Agent, Task

agent_config = load_yaml_file("agents_configuration.yaml")
task_config = load_yaml_file("task_configuration.yaml")
llm = get_llm()


def create_subtopic_retriever_agent():

    subtopic_agent =  Agent(
        role = agent_config['subtopic_retriever_agent']['role'],
        goal = agent_config['subtopic_retriever_agent']['goal'],
        backstory = agent_config['subtopic_retriever_agent']['backstory'],
        verbose = True,
        llm =llm
    )

    subtopic_task = Task(
                description= task_config[
                    "subtopic_identification_task"
                ]["description"],
                expected_output = task_config[
                    "subtopic_identification_task"
                ]["expected_output"],
                agent=subtopic_agent
            )
    return subtopic_agent,subtopic_task