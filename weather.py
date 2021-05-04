import geocoder
import requests
import datetime

import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_BASEURL = "http://api.openweathermap.org/data/2.5"
WEATHER_ONECALL_ENDPOINT = "/onecall" #options:  lat={lat}& lon={lon} & exclude={part} & appid={API key}

g = geocoder.ip("me").latlng



data = requests.get(WEATHER_BASEURL + WEATHER_ONECALL_ENDPOINT + "?lat={}&lon={}&appid={}".format(g[0],g[1],os.environ.get("WEATHER_APIKEY")))

print(g)
print(data.json())
print(os.environ.get("WEATHER_APIKEY"))