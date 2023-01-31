from django.db import models

# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tournament Name')
    related_league_code = models.CharField(max_length=10, verbose_name='Related League Code')
    related_league_link = models.URLField(verbose_name='Related League Link')
    player_capacity = models.IntegerField(verbose_name='Player Capacity')


class Player(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='players', verbose_name='Tournament')
    team_id = models.CharField(max_length=10, unique=True, verbose_name='Team ID')
    team_name = models.CharField(max_length=50, verbose_name='Team name')
    team_region = models.CharField(max_length=50, verbose_name='Region')


class Event(models.Model):
    event_id = models.PositiveIntegerField(verbose_name='Event ID')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='events')
    point = models.IntegerField(default=0, verbose_name='Point')