from django.urls import path
from .views import template

app_name = 'account'

urlpatterns = [
    path('user-sheet/<str:filled_by__telegram_id>/', template.UserSheetView.as_view(), name='user_sheet'),
]
