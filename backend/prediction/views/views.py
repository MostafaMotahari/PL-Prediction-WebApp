from django.views.generic.list import ListView

# Create your views here.
class PredictionView(ListView):
    template_name = 'prediction.html'
    # context_object_name = 'matches'

    # def get_queryset(self):
    #     return Match.objects.all()