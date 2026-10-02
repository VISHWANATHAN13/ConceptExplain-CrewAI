from crewai import Crew, Process
from agents.content_retriever_agent import create_content_retriever_agent
from agents.subtopic_retriever_agent import create_subtopic_retriever_agent
from agents.explanation_agent import create_explanation_agent
from agents.flow_diagram_generator_agent import create_flow_diagram_generator_agent
from agents.final_summarizer_agent import create_final_summarizer_agent

def create_teaching_crew():
    """
    Builds the crew with un-interpolated task templates.
    The user's topic is injected at kickoff time via
    crew.kickoff(inputs={"user_topic": ...}).
    """

    content_retriever_agent, content_retriever_task = create_content_retriever_agent()
    subtopic_retreiver_agent, subtopic_retriever_task = create_subtopic_retriever_agent()
    explanation_agent, explanation_task = create_explanation_agent()
    flow_diagram_agent, flow_diagram_task = create_flow_diagram_generator_agent()
    final_summarizer_agent, final_summarizer_task = create_final_summarizer_agent()
    
    teaching_team = Crew(
        
        agents = [
            content_retriever_agent,
            subtopic_retreiver_agent,
            explanation_agent,
            flow_diagram_agent,
            final_summarizer_agent
        ],
        
        tasks = [
            content_retriever_task,
            subtopic_retriever_task,
            explanation_task,
            flow_diagram_task,
            final_summarizer_task
        ],
        process= Process.sequential,
        verbose = True
    )
    return teaching_team