# imports
import requests
import pandas as pd
from auth import Auth


class Query(Auth):

  def run(self, params: dict, headers: dict = {}):
    host = self.HOST

    base_headers = {
      "X-RapidAPI-Host": host['host'],
      "X-RapidAPI-Key": self.TOKEN
    }
    headers = {**base_headers, **headers}

    print("Running query...")
    resp = requests.request(
      "GET", 
      host["url"], 
      headers = headers, 
      params = params
    )
    print("Query complete!")
    return self.parse_response(resp)


  @staticmethod
  def parse_response(resp, data_path = ['data']):
    try:
      return pd.json_normalize(resp.json(), record_path = data_path)
    except:
      print("failed to parse query, returning raw json response")
      return resp


if __name__ == "__main__":
  from dotenv import load_dotenv # pip install python-dotenv
  import os
  
  # env vars like rapid API token stored in ~/.env
  dotenv_path = os.path.join(os.getenv("HOME"), ".env")
  load_dotenv(dotenv_path = dotenv_path)

  # params
  api = "football-prediction"
  params = {
    "market":"classic",
    "iso_date":"2022-05-21",
    "federation":"UEFA"
  }

  # execute
  q = Query(api)
  res = q.run(params=params)
  print(res)





