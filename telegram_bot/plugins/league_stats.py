from telegram_bot.models import LeagueModel, TemplatesMediaModel
import requests
import os
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from prettytable import PrettyTable

from telegram_bot.plugins.custom_filters import power_mode_filter, banned_filter

# Static variables
BASE_API_URL = "https://fantasy.premierleague.com/api/"

# League data scraper
def league_scraper(message: Message, league_id: int, standing_page: int = 1):
    # Get league data
    # Get classic league from api
    classic_league = requests.get(f"{BASE_API_URL}leagues-classic/{league_id}/standings/?page_standings={standing_page}")

    classic_league = classic_league.json()

    # Sort standings data
    standings_table = PrettyTable(["Rank", "Team", "Full Name", "GW", "Points"])
    # standings_table.max_table_width = 63 # Limit the width for image

    for team in classic_league["standings"]["results"]:
        standings_table.add_row([
            team["rank"],
            team["entry_name"],
            team["player_name"],
            team["event_total"],
            team["total"]
        ])

    # Make the league table image
    template_model = TemplatesMediaModel.objects.first()
    image = Image.open(os.getcwd() + template_model.league_stats_bg.url)
    # image = Image.new("RGB", (600, (len(classic_league["results"]) * 15) + 200), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.getcwd() + template_model.text_font.url, 20)
    draw.text((36, 20), str(standings_table), font=font, fill="black")
    image.save(os.getcwd() + "/media/images/standings.png")  # Saving the created image

    # Inline Keyboard
    inline_keyboard = [[]]

    if standing_page != 1:
        inline_keyboard[0].append(InlineKeyboardButton("Previous Page", callback_data=f"{league_id}:{standing_page - 1}"))

    if classic_league["standings"]["has_next"]:
        inline_keyboard[0].append(InlineKeyboardButton("Next Page", callback_data=f"{league_id}:{standing_page + 1}"))

    # Send the league state as new message
    message.edit_media(
        media=InputMediaPhoto(
            media=os.getcwd() + "/media/images/standings.png",

            caption=f"🏆 **{classic_league['league']['name']} Standings**\n"
            f"➕ Created Date: {classic_league['league']['created']}\n"
            f"▶️ Started GW: {classic_league['league']['start_event']}\n"
            f"📃 __Page {standing_page}__",
        ),

        reply_markup=InlineKeyboardMarkup(inline_keyboard) if len(inline_keyboard[0]) > 0 else None
    )

# Send league stats commands helping text
@Client.on_message(filters.private & (filters.regex("^📊 Stats$") | filters.regex("^/help$")) \
    & power_mode_filter & banned_filter)
def league_help(client: Client, message: Message):
    message.reply_text(
        "🏆 **League Stats**\n\n"
        "➕ To get the default league stats, use the following command:\n"
        "📝 `/leagues`\n\n"
        "➕ To get the custom league stats, use the following command:\n"
        "📝 `/leagues <league_id>` - Get league standings\n"
    )

# Choosing a league to scrap
@Client.on_message(filters.private & filters.command(["leagues"]) & \
    power_mode_filter & banned_filter)
def send_leagues(client: Client, message: Message):
    loading_message = TemplatesMediaModel.objects.first()

    if len(message.text.split(" ")) == 1:
        leagues = LeagueModel.objects.all()

        client.send_animation(
            chat_id=message.chat.id,
            animation=os.getcwd() + loading_message.loading_video.url,
            caption=loading_message.loading_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(league.name, callback_data=league.code)] for league in leagues
            ])
        )

    elif len(message.text.split(" ")) == 2:
        table_message = client.send_animation(
            chat_id=message.chat.id,
            animation=os.getcwd() + loading_message.loading_video.url,
            caption="Please Wait..."
        )
        league_scraper(table_message, int(message.text.split(" ")[1]))

    else:
        message.reply_text("Wrong command format.\n\nUsage: /leagues `[league_id]`")


# Main function that gets league data from fpl api and sort it
@Client.on_callback_query(filters.regex("^[0-9]+") & power_mode_filter & banned_filter)
def get_league_state(client: Client, callback_query: CallbackQuery):

    league_id = int(callback_query.data.split(":")[0])
    standing_page = 1 if len(callback_query.data.split(":")) == 1 else int(callback_query.data.split(":")[1])

    # Send Waiting message
    callback_query.message.edit_caption("Please Wait...")

    # Get league data
    league_scraper(callback_query.message, league_id, standing_page)
