from django.db import models

# Create your models here.
class LeagueModel(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class LoadingModel(models.Model):
    video = models.FileField(upload_to="videos")
    text = models.CharField(max_length=255)

    def __str__(self):
        return "Loading Message"