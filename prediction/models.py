from cgitb import enable
from email.policy import default
from django.db import models

# Create your models here.
class GWModel(models.Model):
    GW_number = models.IntegerField()
    deadline = models.DateTimeField()
    finished = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Gameweek {self.GW_number}"


class TeamModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Team Name')
    logo = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Team Logo')

    def __str__(self):
        return self.name

    def svg_readable_name(self):
        return self.name.lower().replace('_', ' ')


class FixtureModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE , verbose_name='Gameweek', related_name='fixtures')
    fixture_code = models.IntegerField(default=0, verbose_name='Fixture Code')
    home_team = models.ForeignKey(TeamModel, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(TeamModel, on_delete=models.CASCADE, related_name='away_team')
    kickoff_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.home_team} vs {self.away_team}'


class MatchModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE, related_name='matches')
    fixture = models.ForeignKey(FixtureModel, default=None, on_delete=models.CASCADE, related_name='matches')
    team1_score = models.IntegerField(default=0, verbose_name='Team 1 Score')
    team2_score = models.IntegerField(default=0, verbose_name='Team 2 Score')
    prediction = models.ForeignKey('PredictionModel', default=None, on_delete=models.CASCADE, related_name='matches')

    def __str__(self):
        return self.fixture.__str__()


class PredictionModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE, related_name='gw_predictions')
    filled_by = models.ForeignKey('account.User', default=None, on_delete=models.CASCADE, related_name='predictions')
    filled_date_time = models.DateTimeField(auto_now_add=True, verbose_name='Filled Date Time')
    achieved_points = models.IntegerField(default=0, verbose_name='Achieved Points')

    def __str__(self):
        return f'{self.filled_by.username} - {self.GW}'
