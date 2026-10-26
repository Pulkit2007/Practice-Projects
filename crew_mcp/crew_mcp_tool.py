from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

load_dotenv()

llm = LLM(model="gemini/gemini-3.5-flash-lite")

server_params = StdioServerParameters(
    command=r"C:\Users\LENOVO\Practice\.venv\Scripts\python.exe",
    args=[
        "-m",
        "fastmcp",
        "run",
        r"C:\Users\LENOVO\Practice\MCP\weather.py",
        "--transport",
        "stdio",
    ],
)


def get_weather_update(city: str):
    with MCPServerAdapter(server_params) as tools:
        print(
            f"Available tools from MCP STDIO MCP SERVER{[tool.name for tool in tools]}"
        )

        weather_forecast_agent = Agent(
            role="Weather Forecast Analyst",
            goal="Provide a natural language weather update for any city requested by the user, "
            "incorporating all details from the tool output (e.g., weather condition and temperature).",
            backstory="You are a weather forecast assistant specializing in delivering quick and "
            "accurate weather updates using live data, including both temperature and weather conditions.",
            llm=llm,
            tools=tools,
            verbose=True,
    )
        weather_forecast_task = Task(
            description=(
                "Provide a natural language weather update for the city: {city}. "
                "Incorporate all details from the tool output, such as weather condition and temperature, in a complete sentence."
            ),
            expected_output="A natural language sentence summarizing the weather condition and temperature for the requested city.",
            agent=weather_forecast_agent,
    )

        weather_forecast_crew = Crew(
            agents=[weather_forecast_agent],
            tasks=[weather_forecast_task],
            verbose=True,
    )

        # Keep the CrewAI run inside the adapter context so its MCP tools
        # remain connected for the entire request.
        return weather_forecast_crew.kickoff(inputs={"city": city})


if __name__ == "__main__":
    city = "Ludhiana"
    weather = get_weather_update(city)
    print(weather)
