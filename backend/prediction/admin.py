from django.contrib import admin
from .models import GWModel, TeamModel, FixtureModel, MatchModel, PredictionModel

# Register your models here.
class GWAdmin(admin.ModelAdmin):
    list_display = ('GW_number', 'deadline')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')

class FixtureAdmin(admin.ModelAdmin):
    list_display = ('GW', 'home_team', 'away_team', 'date', 'time')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('GW', 'fixture', 'team1_score', 'team2_score')

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('GW', 'filled_date_time')


admin.site.register(GWModel, GWAdmin)
admin.site.register(TeamModel, TeamAdmin)
admin.site.register(FixtureModel, FixtureAdmin)
admin.site.register(MatchModel, MatchAdmin)
admin.site.register(PredictionModel, PredictionAdmin)
