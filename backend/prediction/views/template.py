from django.views.generic.edit import FormView

from prediction.models import FixtureModel, PredictionModel
from prediction.forms import MatchFormSet

# Create your views here.
class PredictionView(FormView):
    model = PredictionModel
    template_name = 'prediction.html'
    form_class = MatchFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fixtures_formset'] = zip(
            FixtureModel.objects.filter(GW__GW_number=1).all(),
            MatchFormSet()
        )
        return context