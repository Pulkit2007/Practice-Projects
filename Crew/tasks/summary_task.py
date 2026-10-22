from crewai import Task
from crew_agents.summary_agent import summary_agent
from tasks.research_task import research_task

summary_task = Task(
    description=(
        "Answer the user's original question:\n\n"
        "{question}\n\n"
        "Use the research task's output as your primary source material. "
        "Identify the most relevant findings, remove irrelevant content "
        "and repetition, compare available evidence, and synthesize "
        "the results into an accurate, easy-to-understand answer.\n\n"
        "Explain technical concepts in simple language. Use headings, "
        "bullet points, numbered steps, or tables when useful. "
        "Preserve relevant source URLs near the claims they support.\n\n"
        "Do not invent information, citations, or conclusions. "
        "Explicitly disclose important uncertainties, conflicting "
        "evidence, and gaps in the research. Do not simply reproduce "
        "the raw scraped content."
    ),
    expected_output=(
        "A polished Markdown response containing:\n"
        "- A direct answer to the user's question\n"
        "- Key findings organized into meaningful sections\n"
        "- Clear explanations and practical steps, when relevant\n"
        "- Relevant source URLs\n"
        "- Important limitations or uncertainties, when necessary\n\n"
        "The answer should be concise, coherent, accurate, and "
        "understandable without requiring the user to read the raw "
        "research output."
    ),
    agent=summary_agent,
    context=[research_task],
)
