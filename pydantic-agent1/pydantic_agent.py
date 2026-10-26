import asyncio
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from fastmcp.client.transports import StdioTransport

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


weather_server = MCPToolset(
    StdioTransport(
        command=r"C:\Users\LENOVO\Practice\.venv\Scripts\python.exe",
        args=[r"C:\Users\LENOVO\Practice\MCP\weather.py"],
    ),
    init_timeout=30,
)

webscraper_server = MCPToolset(
    StdioTransport(
        command=r"C:\Users\LENOVO\Practice\.venv\Scripts\python.exe",
        args=[r"C:\Users\LENOVO\Practice\MCP\webscraper.py"],
    )
)

agent = Agent(
    "google:gemini-3.5-flash-lite",
    toolsets=[weather_server, webscraper_server],
)


async def main():
    async with agent:
        result = await agent.run("what is weather in Chandigarh")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
