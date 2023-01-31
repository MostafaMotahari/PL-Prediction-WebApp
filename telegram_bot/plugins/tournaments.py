from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import filters
import re
import requests
from tournament import models as tour_models


BASE_API_URL = "https://fantasy.premierleague.com/api/"
keyboard = [
    [InlineKeyboardButton("1", callback_data="1"), InlineKeyboardButton("2", callback_data="2"), InlineKeyboardButton("3", callback_data="3")],
    [InlineKeyboardButton("4", callback_data="4"), InlineKeyboardButton("5", callback_data="5"), InlineKeyboardButton("6", callback_data="6")],
    [InlineKeyboardButton("7", callback_data="7"), InlineKeyboardButton("8", callback_data="8"),InlineKeyboardButton("9", callback_data="9")],
    [InlineKeyboardButton("0", callback_data="0"), InlineKeyboardButton("Cancel", callback_data="cancel"), InlineKeyboardButton("Confirm", callback_data="confirm")],
]


@Client.on_message(filters.private & filters.regex("^Tournaments$"))
def get_tournaments(client: Client, message: Message):
    tournaments = tour_models.Tournament.objects.all()
    client.send_message(
        message.chat.id,
        f"There are {len(tournaments)} available tournaments:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(tour.name, callback_data=f"register-{tour.pk}")] for tour in tournaments]
        )
    )


@Client.on_callback_query(filters.regex("^register-(.*)$"))
def register_message(client: Client, query: CallbackQuery):
    tournament = tour_models.Tournament.objects.get(pk=query.data.split("-")[1])
    client.send_message(
        query.message.chat.id,
        f"You're registering in **{tournament.name}** tournament.\n"
        f"Tournament code {tournament.pk}"
        "Please enter your team integer ID:\n"
        "Your ID: ",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


@Client.on_callback_query(filters.regex("^[0-9]$"))
def submit_button(client: Client, query: CallbackQuery):
    pressed_button = "**" + query.data + "**"

    query.message.edit_text(
        query.message.text + pressed_button,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return 1


@Client.on_callback_query(filters.regex("^confirm$"))
def confirm_team_id(client: Client, query: CallbackQuery):
    tournament_pk = re.search(r"Tournament code (.*)", query.message.text)
    query.message.edit_text("__Please wait...__")

    team_id = re.search(r": (.*)", query.message.text)
    team = requests.get(f"{BASE_API_URL}/entry/{team_id}/")
    team = team.json()

    if team['detail'] == "Not found.":
        query.answer("404 Not found!!!")
        return 0

    query.message.edit_text(
        "Is this your team?\n\n"
        f"ID: **{team['id']}**\n"
        f"Team name: {team['name']}\n"
        f"Player name: {team['player_first_name']} {team['player_last_name']}\n"
        f"Overall points: {team['summary_overall_points']}\n"
        f"Overall rank: {team['summary_overall_rank']}\n"
        f"Region: {team['player_region_name']}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Yes, this is!", callback_data=f"confirm_team_id-{team_id}-{tournament_pk}"), InlineKeyboardButton("Hell, No!", callback_data="cancel")]]
        )
    )


@Client.on_callback_query(filters.regex("^confirm_team_id-(.*)-(.*)$"))
def submit_team_id(client: Client, query: CallbackQuery):
    tournament_pk = query.data.splite("-")[2]
    tournament = tour_models.Tournament.get(pk=tournament_pk)
    team_id = query.data.splite("-")[1]
    query.message.edit_text(
        "Alright!\n"
        "Now to compelete your registeration, please join in below league and after that press the 'Joined!' button.\n\n"
        f"Join by code: `{tournament.related_league_code}`\n"
        f"(**Auto Joining Link**)[{tournament.related_league_link}]",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Joined!", caallback_data=f"confirm_joining-{team_id}-{tournament_pk}"), InlineKeyboardButton("Cancel", callback_data="cancel")]]
        )
    )


@Client.on_callback_query(filters.regex("^confirm_joining-(.*)-(.*)$"))
def confirm_joining(client: Client, query: CallbackQuery):
    tournament = tour_models.Tournament.objects.get(pk=query.data.split("-")[2])
    team_id = query.data.splite("-")[1]
    team = requests.get(f"{BASE_API_URL}/entry/{team_id}/")
    team = team.json()

    for league in team['leagues']['classic']:
        if league['id'] == 2441037:
            player = tour_models.Player.create(
                tournament=tournament,
                team_id=team_id,
                team_name=team['name'],
                team_region=team['player_region_name'],
            )

            query.message.edit_text(
                "Congratulations!\n"
                "Your registeration has been successfully completed!\n\n"
                f"Your registeration code is: **{player.pk}**"
            )
            break

    else:
        query.answer("Error! You're not joined in our league yet! Please join and try again.")


@Client.on_callback_query(filters.regex("^cancel$"))
def canel(client: Client, query: CallbackQuery):
    query.message.edit_text("Operation canceled!\n Try again by pressing 'Register' button.")
