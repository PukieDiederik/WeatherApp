# %%
import geocoder
import requests

from dotenv import load_dotenv
load_dotenv()

# %% Call openWeatherMap's onecall api
# exclude should be a string with each section seperated by a comma (no spaces)
def oneCallRequest(apiKey : str, latlng, exclude):
    data = requests.get(f"http://api.openweathermap.org/data/2.5/onecall?lat={latlng[0]}&lon={latlng[1]}&exclude={exclude}&appid={apiKey}").json()
    return data