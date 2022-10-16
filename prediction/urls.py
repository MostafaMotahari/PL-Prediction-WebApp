from django.urls import path

from .views import template

urlpatterns = [
    # path('', template.PredictionView.as_view(), name='prediction'),
    path('<str:token>', template.PredictionView.as_view(), name='prediction'),
]