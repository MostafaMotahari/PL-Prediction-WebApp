from django.db import models

# Create your models here.
class GWModel(models.Model):
    GW_number = models.IntegerField()
    deadline = models.DateTimeField()


class TeamModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Team Name')
    logo = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Team Logo')

    def __str__(self):
        return self.name


class FixtureModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE , verbose_name='Gameweek', related_name='fixtures')
    home_team = models.ForeignKey(TeamModel, on_delete=models.CASCADE)
    away_team = models.ForeignKey(TeamModel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f'{self.home_team} vs {self.away_team}'


class MatchModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE, related_name='matches')
    fixture = models.ForeignKey(FixtureModel, on_delete=models.CASCADE, related_name='matches')
    team1_score = models.IntegerField(default=0, verbose_name='Team 1 Score')
    team2_score = models.IntegerField(default=0, verbose_name='Team 2 Score')

    def __str__(self):
        return self.team1.name + ' vs ' + self.team2.name


class PredictionModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE)
    filled_date_time = models.DateTimeField(auto_now_add=True, verbose_name='Filled Date Time')
    matches = models.ManyToManyField(MatchModel, verbose_name='Matches')
