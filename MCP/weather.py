import os
from dotenv import load_dotenv
import requests
from mcp.server.fastmcp import FastMCP
from datetime import timezone, timedelta, datetime

load_dotenv()

mcp = FastMCP()


@mcp.tool()
def get_weather_forecast(city: str) -> WeatherForecast:
    url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = os.getenv("OPENWEATHER_API_KEY")
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    try:
        if response.status_code == 200:
            print(response)
        else:
            print(response.status_code)
        result = response.json()

        observed_at = datetime.fromtimestamp(
            result["dt"], tz=timezone(timedelta(seconds=result["timezone"]))
        )

        location = (result["name"],)
        description = (result["weather"][0]["description"].capitalize(),)
        temperature_celcius = (result["main"]["temp"],)
        date = observed_at.strftime("%d %B %Y")

    except Exception as e:
        raise Exception(e)

    return f"{location} : {description}, {temperature_celcius}, {date}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
