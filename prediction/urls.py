from django.urls import path

from .views import template

urlpatterns = [
    # path('', template.PredictionView.as_view(), name='prediction'),
    path('form/<str:token>', template.PredictionView.as_view(), name='prediction'),
    path('leaderboard/', template.LeaderboardView.as_view(), name='leaderboard'),
]