from django.views.generic.detail import DetailView
from prediction import models


class UserSheetView(DetailView):
    template_name = 'account/user_sheet.html'
    model = models.PredictionModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prediction"] = self.object.get(GW__GW_number=self.request.GET.get('gw'))
        return context
