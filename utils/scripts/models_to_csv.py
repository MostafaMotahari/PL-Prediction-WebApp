from tournament.models import Player
import csv


with open("players.csv", "w") as csv_file:
    field_names = ["id", "full_name", "telegram_id", "team_id", "team_name", "team_region"]
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(field_names)

    for player in Player.objects.all():
        writer.writerow([player.pk, player.full_name, player.telegram_id, player.team_id, player.team_name, player.team_region])

