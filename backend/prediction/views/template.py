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
        context['formset'] = MatchFormSet()
        context['fixtures'] = FixtureModel.objects.filter(GW=latest_gw)
        
        return context

    def post(self, request, *args, **kwargs):
        formset = MatchFormSet(request.POST)
        # Create a new prediction form for the user
        gw_obj = GWModel.objects.latest('id')
        prediction = PredictionModel.objects.create(GW=gw_obj, filled_by=request.user)

        print("Koooooooon")
        if formset.is_valid():
            for form in formset:
                # Save each match form
                print("Koooooooon")
                instance = form.save(commit=False)
                instance.GW = gw_obj
                instance.fixture = FixtureModel.objects.get(id=form.cleaned_data['fixture_id'])
                instance.save()

                prediction.matches.add(instance)

        print(formset.non_form_errors())
        prediction.save()

        return super().post(request, *args, **kwargs)