from django.views.generic.detail import DetailView
from account import models as account_models


class UserSheetView(DetailView):
    template_name = 'user_sheet.html'
    model = account_models.User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prediction"] = self.object.predictions.get(GW__GW_number=self.request.GET.get('gw'))
        return context
