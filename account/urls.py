from django.urls import path
from .views import template

app_name = 'account'

urlpatterns = [
    path('user-sheet/<int:pk>/', template.UserSheetView.as_view(), name='user_sheet'),
]
