import re
import requests
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tournament import models as tour_models
from telegram_bot.plugins.custom_filters import is_participant_filter, power_mode_filter, banned_filter


BASE_API_URL = "https://fantasy.premierleague.com/api"
keyboard = [
    [InlineKeyboardButton("1", callback_data="1"), InlineKeyboardButton("2", callback_data="2"), InlineKeyboardButton("3", callback_data="3")],
    [InlineKeyboardButton("4", callback_data="4"), InlineKeyboardButton("5", callback_data="5"), InlineKeyboardButton("6", callback_data="6")],
    [InlineKeyboardButton("7", callback_data="7"), InlineKeyboardButton("8", callback_data="8"),InlineKeyboardButton("9", callback_data="9")],
    [InlineKeyboardButton("0", callback_data="0"), InlineKeyboardButton("Clear", callback_data="clear"), InlineKeyboardButton("Confirm", callback_data="confirm")],
]


@Client.on_message(filters.private & filters.regex("^🏆 Tournaments 🏆$") & banned_filter & power_mode_filter)
def get_tournaments(client: Client, message: Message):
    tournaments = tour_models.Tournament.objects.all()
    message_text = "Here are available tournaments that you can register now:\n\n"
    tour_keyboard = []

    for tour in tournaments:
        if tour.has_capacity():
            message_text += f"{tour.pk}. **{tour.name}**\nCapacity: {len(tour.players.all())} of {tour.player_capacity} is completed.\n\n"
            tour_keyboard.append([InlineKeyboardButton(tour.name, callback_data=f"register-{tour.pk}")])

    client.send_message(
        message.chat.id,
        message_text,
        reply_markup=InlineKeyboardMarkup(tour_keyboard)
    )


@Client.on_callback_query(filters.regex("^register-(.*)$") | filters.regex("^clear-(.*)$") & is_participant_filter)
def register_message(client: Client, query: CallbackQuery):
    tournament = tour_models.Tournament.objects.get(pk=query.data.split("-")[1])

    try:
        player = tour_models.Player.objects.get(telegram_id=query.from_user.id)
        confirm_team_id(client, query, player.team_id, tournament.pk)

    except tour_models.Player.DoesNotExist:
        keyboard[3][1].callback_data = f"clear-{tournament.pk}"
        keyboard[3][2].callback_data = f"confirm-{tournament.pk}"

        query.message.edit_text(
            f"⚙️ You're registering in **{tournament.name}** tournament.\n"
            f"🔘 Tournament code **{tournament.pk}**\n"
            "Please enter your team integer ID\n\n"
            "▶️ Your ID: ",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


@Client.on_callback_query(filters.regex("^[0-9]$"))
def submit_button(client: Client, query: CallbackQuery):
    pressed_button = query.data

    query.message.edit_text(
        query.message.text + "**" + pressed_button + "**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return 1


@Client.on_callback_query(filters.regex("^confirm-(.*)$") & is_participant_filter)
def confirm_team_id(client: Client, query: CallbackQuery, team_id=None, tournament_pk=None):
    tournament_pk = tournament_pk or query.data.split("-")[1]
    query.message.edit_text("__Please wait...__")

    team_id = team_id or re.findall("\d+", query.message.text)[1]
    team = requests.get(f"{BASE_API_URL}/entry/{team_id}/")
    team = team.json()

    if team.get('detail', None):
        query.answer("404 Not found!!!")
        return 0

    query.message.edit_text(
        "Is this your team❓\n\n"
        f"🔘 ID: **{team['id']}**\n"
        f"🔘 Team name: {team['name']}\n"
        f"🔘 Player name: {team['player_first_name']} {team['player_last_name']}\n"
        f"🔘 Overall points: {team['summary_overall_points']}\n"
        f"🔘 Overall rank: {team['summary_overall_rank']}\n"
        f"🔘 Region: {team['player_region_name']}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Yes, this is!", callback_data=f"confirm_team_id-{team_id}-{tournament_pk}"), InlineKeyboardButton("Hell, No!", callback_data="cancel")]]
        )
    )


@Client.on_callback_query(filters.regex("^confirm_team_id-(.*)-(.*)$") & is_participant_filter)
def submit_team_id(client: Client, query: CallbackQuery):
    tournament_pk = query.data.split("-")[2]
    tournament = tour_models.Tournament.objects.get(pk=tournament_pk)
    team_id = query.data.split("-")[1]
    query.message.edit_text(
        "☑️ Alright!\n"
        "Now to compelete your registeration, please join in below league and after that press the 'Joined!' button.\n\n"
        f"🔸 Join by code: `{tournament.related_league_invite}`\n"
        f"🔹 **[Auto Joining Link]({tournament.related_league_link})**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Joined!", callback_data=f"confirm_joining-{team_id}-{tournament_pk}"), InlineKeyboardButton("Cancel", callback_data="cancel")]]
        )
    )


@Client.on_callback_query(filters.regex("^confirm_joining-(.*)-(.*)$") & is_participant_filter)
def confirm_joining(client: Client, query: CallbackQuery):
    tournament = tour_models.Tournament.objects.get(pk=query.data.split("-")[2])
    team_id = query.data.split("-")[1]
    team = requests.get(f"{BASE_API_URL}/entry/{team_id}/")
    team = team.json()

    for league in team['leagues']['classic']:
        if league['id'] == int(tournament.related_league_code):
            try:
                player = tour_models.Player.objects.get(telegram_id=query.from_user.id)
                player.tournament.add(tournament)
                player.save()

            except tour_models.Player.DoesNotExist:
                player = tour_models.Player.objects.create(
                    tournament=tournament,
                    full_name=team['player_first_name'] + ' ' + team['player_last_name'],
                    telegram_id=query.from_user.id,
                    team_id=team_id,
                    team_name=team['name'],
                    team_region=team['player_region_name'],
                )

            query.message.edit_text(
                "🎉 Congratulations!\n"
                "✅ Your registeration has been successfully completed!\n\n"
                f"👉 Your registeration code is: **{player.pk}**"
            )

            client.send_message(
                "FBI_Phoenix",
                "A new user has been registered!\n\n"
                f"ID: **{player.team_id}**\n"
                f"Team Name: {player.team_name}\n"
                f"Full Name: {player.full_name}\n"
                f"Overall: {team['summary_overall_rank']}\n\n"
                f"PV: [{player.full_name}](tg://user?id={player.telegram_id})",
            )
            break

    else:
        query.answer("Error! You're not joined in our league yet! Please join and try again.")


@Client.on_callback_query(filters.regex("^cancel$"))
def canel(client: Client, query: CallbackQuery):
    query.message.edit_text("Operation canceled!\n Try again by pressing 'Register' button.")
