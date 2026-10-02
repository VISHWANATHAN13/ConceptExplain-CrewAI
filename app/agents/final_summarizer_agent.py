# import yaml
from agents.agents_config import load_yaml_file
from llm_config.load_llm import get_llm
from crewai import Agent, Task

agent_config = load_yaml_file("agents_configuration.yaml")
task_config = load_yaml_file("task_configuration.yaml")
llm = get_llm()
def create_final_summarizer_agent():

    final_document_agent = Agent(
        role = agent_config['final_summarizer_agent']['role'],
        goal = agent_config['final_summarizer_agent']['goal'],
        backstory = agent_config['final_summarizer_agent']['backstory'],
        verbose = True,
        llm =llm
    )

    final_document_task = Task(
                        description= task_config[
                            "final_document_task"
                        ]["description"],
                        expected_output = task_config[
                            "final_document_task"
                        ]["expected_output"],
                        agent=final_document_agent
                    )
    return final_document_agent,final_document_task