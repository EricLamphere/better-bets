# imports
import requests
from auth import Auth
from utils.dates import server_to_local_datetime

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


    def print_match_predictions(self, data):
        for match in data:
          output = "{home} (Home) vs {away} (Away)\n\t- Start Time: {start}\n\t- Prediction: {pred} (odds: {odds}, prob: {prob})\n\t- {oo}"

          local_start_time = server_to_local_datetime(match["start_date"])
          home_team = match["home_team"]
          away_team = match["away_team"]
          prediction = match["prediction"]
          winner = self._prediction_enum(prediction, home_team, away_team)
          if "odds" in match:
              prediction_odds = match["odds"].get(prediction, None)
              prediction_prob = self.prob_from_odds(prediction_odds, True)
              odds = {self._prediction_enum(k):v for (k,v) in match["odds"].items()}#  if k != _prediction_enum(prediction)}
          else:
              # user is not able to see odds as it's subscription plan does not support it.
              prediction_odds = "Access Denied"
              prediction_prob = "Access Denied"
              odds = "Access Denied"

          print(output.format(
            start = local_start_time, 
            home = home_team, 
            away = away_team, 
            pred = winner, 
            odds = prediction_odds,
            prob = prediction_prob,
            oo = odds
          ))
      
    @staticmethod
    def prob_from_odds(odds, formatted = False):
        prob = odds / (1 + odds)
        if formatted:
            return f"{round(prob * 100, 2)}%"
        else:
            return prob


    @staticmethod
    def _prediction_enum(prediction, home = None, away = None):
        if home == None:
            home = "Home"
        if away == None:
            away = "Away"

        if prediction == "1":
            return home
        elif prediction == "2":
            return away
        elif prediction == "X":
            return "Draw"
        elif prediction in ("1X", "X1"):
            return f"{home} or Draw"
        elif prediction in ("2X", "X2"):
            return f"{away} or Draw"
        elif prediction == "12":
            return f"{home} or {away}"
        else:
            raise Exception(f"Unknown prediction value: {prediction}")


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
    q.print_match_predictions(res)





