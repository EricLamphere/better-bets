import json, os

class Auth:
  def __init__(self, api: str, token: str = None):
    self.API = api.replace("-", "_").upper()
    self.TOKEN = self.get_token(token)
    self.HOST = self.get_api_info()


  def get_api_info(self):
    api = self.API
    hosts = json.load(open("./src/rapid_api/hosts.json"))
    if api not in hosts.keys():
      raise Exception(f"{api} is not yet supported")
    return hosts[api]
  

  @staticmethod
  def get_token(token: str = None):
    env_token = os.getenv("RAPID_API_TOKEN")
    
    if token != None:
      return token
    elif env_token != None:
      return env_token
    else:
      raise Exception(
        """
        Must provide a token with one of the following methods:
          * RAPID_API_TOKEN environment variable
          * Explicitly defined during Authentication
        """
      )