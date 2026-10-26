import os
from pathlib import Path
from dotenv import load_dotenv
import requests
# Use the FastMCP implementation shipped with the MCP version required by
# CrewAI. This avoids a separate FastMCP package causing protocol mismatches.
from mcp.server.fastmcp import FastMCP
from datetime import timezone, timedelta, datetime

# Load the project environment even when the server is launched by an MCP client.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Give the server a stable name for MCP clients.
mcp = FastMCP("WeatherServer")

@mcp.tool()
def get_weather_forecast(city: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY is not set in .env file."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            message = response.json().get("message", response.text)
            return f"OpenWeather request failed ({response.status_code}): {message}"

        result = response.json()
        observed_at = datetime.fromtimestamp(
            result["dt"], tz=timezone(timedelta(seconds=result["timezone"]))
        )
        location = result["name"]
        description = result["weather"][0]["description"].capitalize()
        temperature_celsius = result["main"]["temp"]
        date = observed_at.strftime("%d %B %Y")

        return f"{location}: {description}, {temperature_celsius}°C, {date}"
    except requests.RequestException as error:
        return f"Error fetching weather data: {error}"

if __name__ == "__main__":
    mcp.run(transport="stdio")