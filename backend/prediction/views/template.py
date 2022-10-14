from django.views.generic.edit import FormView

from prediction.models import FixtureModel, PredictionModel, GWModel
from prediction.forms import MatchFormSet

# Create your views here.
class PredictionView(FormView):
    model = PredictionModel
    template_name = 'prediction.html'
    form_class = MatchFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_gw = GWModel.objects.latest('id')
        context['fixtures_formset'] = zip(
            FixtureModel.objects.filter(GW=latest_gw).all(),
            MatchFormSet()
        )
        return context

    def post(self, request, *args, **kwargs):
        formset = MatchFormSet(request.POST)
        # Create a new prediction form for the user
        prediction = PredictionModel.objects.create()
        gw_obj = GWModel.objects.latest('id')
        prediction.GW = gw_obj
        prediction.filled_by = request.user

        if formset.is_valid():
            for form in formset:
                # Save each match form
                instance = form.save(commit=False)
                instance.GW = gw_obj
                instance.fixture = FixtureModel.objects.get(id=form.cleaned_data['fixture_id'])
                instance.save()

                prediction.matches.add(instance)

        prediction.save()

        return super().post(request, *args, **kwargs)