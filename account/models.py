from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="Phone Number")
    card_number = models.CharField(max_length=16, blank=True, null=True, verbose_name="Card Number")
    telegram_id = models.CharField(max_length=11, blank=True, null=True, verbose_name="Telegram ID")
    status = models.CharField(max_length=10, default="user", verbose_name="Status")
    prediction_token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Prediction Token")
    total_prediction_points = models.IntegerField(default=0, verbose_name="Total Prediction Points")
    monthly_prediction_points = models.IntegerField(default=0, verbose_name="Monthly Prediction Points")
    weekly_prediction_points = models.IntegerField(default=0, verbose_name="Weekly Prediction Points")
