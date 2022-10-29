from account.models import User
from prediction.models import GWModel, FixtureModel, TeamModel
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
import requests

# Static variables
BASE_API_URL = "https://fantasy.premierleague.com/api/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}


def disable_gw_after_deadline():
    latest_gw = GWModel.objects.latest("id")
    if latest_gw.enabled and latest_gw.deadline < timezone.now():
        latest_gw.enabled = False
        latest_gw.save()

        for user in User.objects.all():
            user.weekly_prediction_points = 0
            user.save()

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

    response = requests.get(BASE_API_URL + "bootstrap-static/", headers=HEADERS).json()

    if not response["events"][latest_gw.GW_number - 1]["finished"] or latest_gw.finished:
        return

    predictions = latest_gw.gw_predictions.all()

    if not predictions:
        return
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

    latest_gw.finished = True
    latest_gw.save()

    update_fixtures()

    return True


def start_updater_job():
    scheduler = BackgroundScheduler(timezone="Asia/Tehran")
    scheduler.add_job(calculate_points, "cron", hour=0, minute=0)
    scheduler.add_job(disable_gw_after_deadline, "interval", hours=1)
    scheduler.start()