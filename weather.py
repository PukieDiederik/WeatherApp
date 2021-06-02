# %%
import PyQt5
import geocoder
import requests
import gui
import os

from dotenv import load_dotenv
load_dotenv()

# %% Call openWeatherMap's onecall api
# exclude should be a string with each section seperated by a comma (no spaces)
def oneCallRequest(apiKey : str, latlng, exclude):
    data = requests.get(f"http://api.openweathermap.org/data/2.5/onecall?lat={latlng[0]}&lon={latlng[1]}&exclude={exclude}&units=metric&appid={apiKey}").json()
    return data

# %% Get data
data = oneCallRequest(os.environ.get("WEATHER_APIKEY"), geocoder.ip("me").latlng, "minutely,alerts")

# %% Start GUI
app = PyQt5.QtWidgets.QApplication([])
app.setStyleSheet(open("./Resources/stylesheets/WeatherApp.css").read())

main = gui.WeatherApp() #initializes everything in the window
main.setWeatherIcon(data["current"]["weather"][0]["icon"])
main.setWeatherName(data["current"]["weather"][0]["description"])
main.setTemperature(data["current"]["temp"],data["current"]["feels_like"])

for i in range(len(data["hourly"])):
    item = data["hourly"][i]
    main.addHOElement(gui.hourlyOverview(main, item["weather"][0]["icon"], item["pop"], item["dt"], item["temp"], item["feels_like"]))

for i in range(len(data["daily"])):
    item = data["daily"][i]
    main.addDOElement(gui.dailyOverview(main, item["weather"][0]["icon"], item["weather"][0]["main"], item["dt"], item["temp"]["day"], item["feels_like"]["day"], item["pop"]))

main.setCloudiness(data["current"]["clouds"])
main.setUVI(data["current"]["uvi"])
main.setWind(data["current"]["wind_deg"], data["current"]["wind_speed"])

app.exec_()
# %%
