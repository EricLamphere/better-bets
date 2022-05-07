import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

#params = {
url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
querystring = {
  "market":"classic",
  "iso_date":"2018-12-01",
  "federation":"UEFA"
}
headers = {
"X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com",
"X-RapidAPI-Key": os.getenv("RAPID_API_KEY")
}
#}

resp = requests.request("GET", url, headers=headers, params=querystring)
resp_df = pd.json_normalize(resp.json(), record_path = ['data'])
# resp = json.loads(response_json.json())

print(resp_df.head())

