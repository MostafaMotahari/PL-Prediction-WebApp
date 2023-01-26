from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.core import paginator
from django.shortcuts import render
from config.settings import ALLOWED_HOSTS
from django.utils import timezone
import urllib
import requests
from account.models import User

from prediction.models import FixtureModel, PredictionModel, GWModel
from prediction.forms import MatchFormSet
from prediction.mixins import TokenValidationMixin


# Create your views here.
class PredictionView(TokenValidationMixin, FormView):
    model = PredictionModel
    template_name = 'prediction.html'
    form_class = MatchFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Note that the deadline is 30 minutes before the actual deadline and it controlled in telegram_bot/plugins/prediction.py
        latest_gw = GWModel.objects.get(enabled=True)
        context['game_week'] = latest_gw
        context['fixtures'] = FixtureModel.objects.filter(GW=latest_gw)
        context['formset'] = MatchFormSet()
        return context

    def post(self, request, *args, **kwargs):
        formset = MatchFormSet(request.POST)
        # Create a new prediction form for the user
        gw_obj = GWModel.objects.latest('id')
        prediction = PredictionModel.objects.create(GW=gw_obj, filled_by=request.user)

        if formset.is_valid():
            for form in formset:
                # Save each match form
                instance = form.save(commit=False)
                instance.GW = gw_obj
                print(form.cleaned_data)
                instance.fixture = FixtureModel.objects.get(id=form.cleaned_data['fixture_id'])
                instance.prediction = prediction
                instance.save()

            prediction.save()
            request.user.token_expiry = timezone.now()
            request.user.save()

            # Send the sheet details in channel
            user_sheet_url = f"http://{ALLOWED_HOSTS[0]}/user-sheet/{request.user.telegram_id}?gw{gw_obj.GW_number}"
            user_sheet_notify = f"{request.user.username}'s prediction for week {gw_obj.GW_number} was successfully registered!\n\n(Check it out now in website!)[{user_sheet_url}]\n\nSubmit your prediction now -> @PLPredictionBot"
            requests.get('' + urllib.parse.quote(user_sheet_notify))

            return render(request, 'successful_predict.html')

        print(formset.errors)
        print(formset.non_form_errors())
        return render(request, 'failed.html')


# Leaderboard
class LeaderboardView(ListView):
    model = User
    template_name = 'leaderboard.html'

    def get_context_data(self, **kwargs):
        users_total_points = User.objects.order_by('-total_prediction_points')
        users_total_points_paginator = paginator.Paginator(users_total_points, 20)
        users_weekly_points = User.objects.order_by('-weekly_prediction_points')
        users_weekly_points_paginator = paginator.Paginator(users_weekly_points, 20)

        page_number = self.request.GET.get('page')
        total_points_page_obj = users_total_points_paginator.get_page(page_number)
        weekly_points_page_obj = users_weekly_points_paginator.get_page(page_number)

        context = super().get_context_data(**kwargs)
        context['total_points_leaderboard'] = total_points_page_obj
        context['weekly_points_leaderboard'] = weekly_points_page_obj
        return context

