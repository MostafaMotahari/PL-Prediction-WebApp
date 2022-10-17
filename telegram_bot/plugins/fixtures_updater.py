from urllib import response
from prediction.models import GWModel, FixtureModel, TeamModel, MatchModel, PredictionModel
import requests

# Static variables
BASE_API_URL = "https://fantasy.premierleague.com/api/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}

def need_update_and_calculate():
    try: latest_gw = GWModel.objects.latest("id") 
    except: return None

    response = requests.get(BASE_API_URL + "bootstrap-static/", headers=HEADERS).json()

    if response["events"][latest_gw.id - 1]["is_finished"]:
        latest_gw.is_finished = True
        latest_gw.save()
        return True
    return False


def update_fixtures():
    # Create next GW object
    response = requests.get(BASE_API_URL + "bootstrap-static/", headers=HEADERS).json()

    for event in response["events"]:
        if event["is_next"] == True:
            latest_gw = GWModel.objects.create(
                GW_number=event["id"],
                deadline=event["deadline_time"]
            )
            latest_gw.save()

    # Update fixtures
    response = requests.get(BASE_API_URL + "fixtures/", headers=HEADERS).json()

    for fixture in response:
        if fixture["event"] == latest_gw.GW_number:
            FixtureModel.objects.create(
                GW=latest_gw,
                fixture_code=fixture["code"],
                home_team=TeamModel.objects.get(id=fixture["team_h"]),
                away_team=TeamModel.objects.get(id=fixture["team_a"]),
                kickoff_time=fixture["kickoff_time"],
            )


def calculate_points():
    latest_gw = GWModel.objects.latest("id")
    predictions = latest_gw.gw_predictions.all()
    response = requests.get(BASE_API_URL + "fixtures/", headers=HEADERS).json()

    for prediction in predictions:
        for match in prediction.matches.all():
            json_fixture = next((fixture for fixture in response if fixture["code"] == match.fixture.fixture_code), None)
            
            # The user has made the prediction completely accurately
            if json_fixture["team_h_score"] == match.team1_score and json_fixture["team_a_score"] == match.team2_score:
                prediction.achieved_points += 3

            # The user just predicted the difference correctly
            elif json_fixture["team_h_score"] - json_fixture["team_a_score"] == match.team1_score - match.team2_score:
                prediction.achieved_points += 2

            # The user just predicted the winner correctly
            # Another way to do this is to just look at the mathematical sign of the difference between the actual and user predicted goals.
            elif json_fixture["team_h_score"] > json_fixture["team_a_score"] and match.team1_score > match.team2_score:
                prediction.achieved_points += 1

            elif json_fixture["team_h_score"] < json_fixture["team_a_score"] and match.team1_score < match.team2_score:
                prediction.achieved_points += 1

        prediction.save()
        prediction.filled_by.weekly_prediction_points = prediction.achieved_points
        prediction.filled_by.total_prediction_points += prediction.achieved_points
        prediction.filled_by.save()

    return True
                    

def updater_and_calculator():
    if need_update_and_calculate():
        calculate_points()
        update_fixtures()
        return True
    return False