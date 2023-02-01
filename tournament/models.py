from django.db import models

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tournament Name')
    related_league_invite = models.CharField(max_length=10, verbose_name='Related League Invite')
    related_league_code = models.IntegerField(default=0, verbose_name='Related League Code')
    related_league_link = models.URLField(verbose_name='Related League Link')
    player_capacity = models.IntegerField(verbose_name='Player Capacity')

    def __str__(self):
        return self.name

    def has_capacity(self):
        return True if len(self.players.all()) < self.player_capacity else False


class Player(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='players', verbose_name='Tournament')
    full_name = models.CharField(max_length=100, verbose_name='Full Name')
    telegram_id = models.CharField(max_length=20, unique=True, verbose_name='Telegram ID')
    team_id = models.CharField(max_length=10, unique=True, verbose_name='Team ID')
    team_name = models.CharField(max_length=50, verbose_name='Team name')
    team_region = models.CharField(max_length=50, verbose_name='Region')

    def __str__(self):
        return self.full_name


class Event(models.Model):
    event_id = models.PositiveIntegerField(verbose_name='Event ID')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='events')
    point = models.IntegerField(default=0, verbose_name='Point')
