from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# class PredictionView(ListView):
#     template_name = 'prediction.html'

def sample(request):
    return render(request, 'prediction.html')