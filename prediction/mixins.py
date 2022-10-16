from account.models import User
from django.http import HttpResponseRedirect
from time import timezone


class TokenValidationMixin:
    """ This WebApp uses token to allow the user to predict fixtures.
    The feature helps us prevent unauthorized access to a user's predictions.
    This mixin validates the token and returns a 403 if the token is invalid."""

    def validate_token(self, token):
        try:
            user = User.objects.get(prediction_token=token)
            if user.token_expiry > timezone.now():
                return True
        except User.DoesNotExist:
            pass
        return False

    def handle_no_permission(self):
        return HttpResponseRedirect("/")

    def dispatch(self, request, *args, **kwargs):
        if not self.validate_token(request.GET.get("token")):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)