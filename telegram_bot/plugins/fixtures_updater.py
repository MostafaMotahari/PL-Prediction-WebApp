from wsgiref.simple_server import demo_app
from prediction.models import GWModel, FixtureModel, TeamModel
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
import requests

# Static variables
BASE_API_URL = "https://fantasy.premierleague.com/api/"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}

def need_to_update_fixtures():
    try: latest_gw = GWModel.objects.latest("id") 
    except: return True

    response = requests.get(BASE_API_URL + "bootstrap-static/", headers=HEADERS).json()

    for event in response["events"]:
        if event["is_next"] == True:
            if latest_gw.GW_number == event["id"]:
                return False

    return True


@Client.on_callback_query(filters.regex("^update_fixture$"))
def update_fixtures(client: Client, callback_query: CallbackQuery):
    if not need_to_update_fixtures():
        callback_query.answer("Fixtures are already up to date!", show_alert=True)
        return False

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
                home_team=TeamModel.objects.get(id=fixture["team_h"]),
                away_team=TeamModel.objects.get(id=fixture["team_a"]),
                kickoff_time=fixture["kickoff_time"],
            )

    callback_query.edit_message_text("Fixtures updated successfully!")