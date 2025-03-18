import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

owm_api_key = os.environ.get("OWM_API_KEY")
parameters = {
    "lat": 6.524379,
    "lon": 3.379206,
    "appid": owm_api_key,
    "cnt": 4,
}
account_sid = os.environ.get("TWILIO_ACC_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()
#print(weather_data["list"][0]["weather"][0])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https": os.environ["https_proxy"]}

    client = Client(account_sid,auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today, remember to carry an umbrella🌂",
        from_="+19082578642",
        to="+2348165603866",
    )
    print(message.status)