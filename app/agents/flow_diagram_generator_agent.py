# import yaml
from agents.agents_config import load_yaml_file
from llm_config.load_llm import get_llm
from crewai import Agent, Task

agent_config = load_yaml_file("agents_configuration.yaml")
task_config = load_yaml_file("task_configuration.yaml")
llm = get_llm()
def create_flow_diagram_generator_agent():

    flow_diagram_agent =  Agent(
        role = agent_config['flow_diagram_generator_agent']['role'],
        goal = agent_config['flow_diagram_generator_agent']['goal'],
        backstory = agent_config['flow_diagram_generator_agent']['backstory'],
        verbose = True,
        llm =llm
    )

    flow_diagram_task = Task(
                    description= task_config[
                        "flow_diagram_task"
                    ]["description"],
                    expected_output = task_config[
                        "flow_diagram_task"
                    ]["expected_output"],
                    agent=flow_diagram_agent
                )
    return flow_diagram_agent,flow_diagram_task