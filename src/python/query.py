# imports
import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

# pw = Query.name
# pw2 = Query().name


class Query:
  name = "Eric is cool"
  def __init__(self, api, params):
    self.api = api.replace("-", "_").upper()
    self.params = params
    self.token = os.getenv("RAPID_API_TOKEN")
  
  @staticmethod
  def get_api_info(self):
    hosts = json.load(open("./src/rapid_api/hosts.json"))
    host = hosts[self.api]
    return host
  
  @classmethod
  def query(cls, params):
    host = self.get_api_info()
    
    headers = {
      "X-RapidAPI-Host": host['host'],
      "X-RapidAPI-Key": self.token
    }
    
    resp = requests.request(
      "GET", 
      host.get("url"), 
      headers = headers, 
      params = params
    )
    resp_df = pd.json_normalize(resp.json(), record_path = ['data'])
    return resp_df



if __name__=="__main__":
  # env vars stored in ~/.env
  load_dotenv(dotenv_path = os.path.join(os.getenv("HOME"), ".env"))
  # os.getenv("RAPID_API_TOKEN")
  
  # params
  api = "football-prediction"
  params = {
    "market":"classic",
    "iso_date":"2018-12-01",
    "federation":"UEFA"
  }
  
  # execute
  q = Query(api, params)
  q.query(params=params)

  print(res.head())





