import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from fastmcp import FastMCP
from datetime import timezone, timedelta, datetime

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

mcp = FastMCP()


@mcp.tool()
def get_weather_forecast(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is not configured")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params, timeout=15)
    if response.status_code != 200:
        try:
            message = response.json().get("message", response.text)
        except ValueError:
            message = response.text
        raise RuntimeError(f"OpenWeather request failed ({response.status_code}): {message}")

    result = response.json()
    observed_at = datetime.fromtimestamp(
        result["dt"], tz=timezone(timedelta(seconds=result["timezone"]))
    )
    location = result["name"]
    description = result["weather"][0]["description"].capitalize()
    temperature_celsius = result["main"]["temp"]
    date = observed_at.strftime("%d %B %Y")

    return f"{location}: {description}, {temperature_celsius}°C, {date}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
