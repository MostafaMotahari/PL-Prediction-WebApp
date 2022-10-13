from django.urls import path

from .views import template

urlpatterns = [
    # path('', template.PredictionView.as_view(), name='prediction'),
    path('', template.sample, name='prediction'),
]