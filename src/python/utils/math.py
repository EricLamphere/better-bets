

def prob_from_odds(odds, formatted = False):
    prob = odds / (1 + odds)
    if formatted:
        return f"{round(prob * 100, 2)}%"
    else:
        return prob