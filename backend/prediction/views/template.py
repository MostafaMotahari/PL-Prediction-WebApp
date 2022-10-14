from django.views.generic.edit import CreateView

from prediction.models import MatchModel, FixtureModel
from prediction.forms import MatchFormSet

# Create your views here.
class PredictionView(CreateView):
    model = MatchModel
    template_name = 'prediction.html'

    def get_context_data(self, **kwargs):
        context = super(MatchModel, self).get_context_data(**kwargs)
        context['fixtures'] = FixtureModel.objects.filter(GW__GW_number=1)
        context['formset'] = MatchFormSet()

        return context