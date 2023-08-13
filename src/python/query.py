# imports
import requests
from auth import Auth

class Query(Auth):

    def run(self, params: dict, headers: dict = {}):
        host = self.HOST

        base_headers = {
          "X-RapidAPI-Host": host['host'],
          "X-RapidAPI-Key": self.TOKEN
        }
        headers = {**base_headers, **headers}

        session = requests.Session()
        session.headers = headers

        response = session.get(host["url"], params=params)
        response_validated = self._validate_response(response)
        return self._parse_response(response_validated)
    

    @staticmethod
    def _validate_response(response):
        if response.ok:
          return response
        else:
          raise Exception(
            f"""
            Bad response from server, status-code: {response.status_code}
            {response.content}
            """
          )


    @staticmethod
    def _parse_response(response):
        parsed = response.json()["data"]
        parsed.sort(key=lambda p: p["start_date"])
        return parsed



if __name__ == "__main__":
    from dotenv import load_dotenv # pip install python-dotenv
    import os

    # env vars like rapid API token stored in ~/.env
    dotenv_path = os.path.join(os.getenv("HOME"), ".env")
    load_dotenv(dotenv_path = dotenv_path)

    # params
    api = "football-prediction"
    params = {
      "market": "classic",
      "iso_date": "2023-08-12",
      "federation": "UEFA"
    }

    # execute
    q = Query(api)
    res = q.run(params=params)
    print(res)





