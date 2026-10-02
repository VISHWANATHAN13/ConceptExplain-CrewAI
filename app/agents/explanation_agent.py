# import yaml
from agents.agents_config import load_yaml_file
from llm_config.load_llm import get_llm
from crewai import Agent, Task

agent_config = load_yaml_file("agents_configuration.yaml")
task_config = load_yaml_file("task_configuration.yaml")
llm = get_llm()


def create_explanation_agent():

    explanation_agent =  Agent(
        role = agent_config['explanation_agent']['role'],
        goal = agent_config['explanation_agent']['goal'],
        backstory = agent_config['explanation_agent']['backstory'],
        verbose = True,
        llm =llm
    )

    explanation_task = Task(
            description= task_config[
                "explanation_task"
            ]["description"],
            expected_output = task_config[
                "explanation_task"
            ]["expected_output"],
            agent=explanation_agent
        )
    return explanation_agent,explanation_task