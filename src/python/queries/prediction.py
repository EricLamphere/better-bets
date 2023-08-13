from query import Query
from utils.dates import server_to_local_datetime
from utils.math import prob_from_odds

API = "football-prediction"
BASE_PARAMS = {
  "market": "classic",
  # "iso_date": "2023-08-12",
  "federation": "UEFA"
}

def query_predictions(date):
    params = {**BASE_PARAMS, "iso_date": date}
    q = Query(API)
    return q.run(params=params)

def match_prediction(date, team):
    data = query_predictions(date)
    return _get_match_predictions(data, team)

def _get_match_predictions(data, team = None):
    if team == None:
        res = data

    for match in data:
        local_start_time = server_to_local_datetime(match["start_date"])
        home_team = match["home_team"]
        away_team = match["away_team"]
        if team != None: 
            if team not in (home_team, away_team):
                continue
            else:
                res = match
        
        prediction = match["prediction"]
        predicted_winner = _prediction_enum(prediction, home_team, away_team)
        if "odds" in match:
            prediction_odds = match["odds"].get(prediction, None)
            prediction_prob = prob_from_odds(prediction_odds, True)
            odds = {_prediction_enum(k):v for (k,v) in match["odds"].items()}#  if k != _prediction_enum(prediction)}
        else:
            prediction_odds = "Access Denied"
            prediction_prob = "Access Denied"
            odds = "Access Denied"
        
        if "result" in match:
            score = match["result"]
            result = f"{home_team} ({score}) {away_team}"
        else:
            result = "No result yet"

        output = "{home} (Home) vs {away} (Away)"
        output += "\n\t- Start Time: {start}\n\t- Prediction: {pred} (odds: {odds}, prob: {prob})"
        output += "\n\t- Result: {result}\n\t- Other Odds: {oo}"
      
        print(output.format(
          start = local_start_time, 
          home = home_team,
          away = away_team,
          id = id,
          pred = predicted_winner,
          odds = prediction_odds,
          prob = prediction_prob,
          oo = odds,
          result = result
        ))
    return res


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
    res = match_prediction("2023-08-12", "Arsenal")
    print(res)



