from django.db import models

# Create your models here.
class LeagueModel(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TemplatesMediaModel(models.Model):
    loading_video = models.FileField(upload_to="videos/")
    loading_text = models.TextField()
    league_stats_bg = models.FileField(upload_to="images/")
    captain_stats_bg = models.FileField(upload_to="images/")
    text_font = models.FileField(upload_to="files/" ,default="files/Roboto-Regular.ttf")

    def __str__(self):
        return "Loading Media"