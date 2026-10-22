from crewai import Crew, Process
from crew_agents.research_agent import research_agent
from crew_agents.summary_agent import summary_agent
from tasks.research_task import research_task
from tasks.summary_task import summary_task

crew = Crew(
    agents=[research_agent, summary_agent],
    tasks=[research_task, summary_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(
    inputs={"question": "How does retrieval-augmented generation work?"}
)

print(result)
