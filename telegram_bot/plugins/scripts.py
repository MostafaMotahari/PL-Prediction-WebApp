import csv
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from tournament.models import Player
from custom_filters import admin_filter


@Client.on_message(filters.private & filters.regex("^/player_csv$") & admin_filter)
def get_player_csv_file(client: Client, message: Message):
    msg = message.reply_text("Please wait ...")
    with open("players.csv", "w") as csv_file:
        field_names = ["id", "full_name", "telegram_id", "team_id", "team_name", "team_region"]
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(field_names)

        for player in Player.objects.all():
            writer.writerow([player.pk, player.full_name, player.telegram_id, player.team_id, player.team_name, player.team_region])

    msg.delete()
    client.send_document(
        message.chat.id,
        "players.csv"
    )
