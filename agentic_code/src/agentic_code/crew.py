import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_ollama import ChatOllama
from crewai_tools import FileReadTool

# Set environment variables to prevent CrewAI from looking for OpenAI
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OTEL_SDK_DISABLED"] = "true"

@CrewBase
class AgenticCodeCrew():
    """AgenticCode crew for Multi-Agent Coding"""

    # 1. Define LLMs with high timeout for your i5-1235U
    # Using the exact names from your 'ollama list'
    local_llm = ChatOllama(
        model="qwen2.5-coder:7b", 
        base_url="http://localhost:11434/v1",
        timeout=300
    )
    
    reviewer_llm = ChatOllama(
        model="llama3.2:latest", 
        base_url="http://localhost:11434/v1",
        timeout=300
    )

    # --- AGENTS ---

    @agent
    def coder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['coder_agent'],
            llm=self.local_llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def reviewer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer_agent'],
            llm=self.reviewer_llm,
            verbose=True,
            allow_delegation=False
        )

    # --- TASKS ---
    # These must match the keys in your tasks.yaml exactly

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
           
        )

    # --- CREW ---

    @crew
    def crew(self) -> Crew:
        """Creates the AgenticCode crew"""
        return Crew(
            agents=self.agents,             # Automatically collects functions with @agent
            tasks=self.tasks,               # Automatically collects functions with @task
            process=Process.sequential,     # Runs tasks one after the other
            manager_llm=self.local_llm,     # Prevents OpenAI 401 error
            verbose=True
        )