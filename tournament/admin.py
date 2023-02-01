from django.contrib import admin
from . import models

# Register your models here.
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'related_league_code', 'player_capacity', )


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team_name', 'team_region')


admin.site.register(models.Tournament, TournamentAdmin)
