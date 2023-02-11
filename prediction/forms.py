from .models import MatchModel
from django import forms


class MatchForm(forms.ModelForm):
    fixture_id = forms.IntegerField(widget=forms.HiddenInput())
    team1_score = forms.IntegerField(widget=forms.NumberInput(attrs={
        'title': 'Score Value',
        'value': 0,
        'id': 'teamScore',
        'class': 'js_team_score score-value-input',
        'min': 0,
        'max': 20,
    }))
    team2_score = forms.IntegerField(widget=forms.NumberInput(attrs={
        'title': 'Score Value',
        'value': 0,
        'id': 'teamScore',
        'class': 'js_team_score score-value-input',
        'min': 0,
        'max': 20,
    }))

    class Meta:
        model = MatchModel
        fields = ['team1_score', 'team2_score']


MatchFormSet = forms.formset_factory(MatchForm, extra=20)
