from .models import MatchModel
from django import forms


class MatchForm(forms.ModelForm):
    fixture_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = MatchModel
        fields = ['team1_score', 'team2_score']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['team1_score'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Team 1 Score'})
    #     self.fields['team2_score'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Team 2 Score'})


MatchFormSet = forms.formset_factory(MatchForm, extra=20)