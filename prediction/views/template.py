from cgitb import enable
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.utils import timezone

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

            return render(request, 'successful_predict.html')

        print(formset.errors)
        print(formset.non_form_errors())
        return render(request, 'failed.html')