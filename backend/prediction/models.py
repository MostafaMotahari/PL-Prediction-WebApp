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


class MatchModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE)
    team1 = models.ForeignKey(TeamModel, on_delete=models.CASCADE, related_name='team1', verbose_name='Team 1')
    team1_score = models.IntegerField(default=0, verbose_name='Team 1 Score')
    team2 = models.ForeignKey(TeamModel, on_delete=models.CASCADE, related_name='team2', verbose_name='Team 2')
    team2_score = models.IntegerField(default=0, verbose_name='Team 2 Score')
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.team1.name + ' vs ' + self.team2.name


class PredictionModel(models.Model):
    GW = models.ForeignKey(GWModel, on_delete=models.CASCADE)
    filled_date_time = models.DateTimeField(auto_now_add=True, verbose_name='Filled Date Time')
    matches = models.ManyToManyField(MatchModel, verbose_name='Matches')
