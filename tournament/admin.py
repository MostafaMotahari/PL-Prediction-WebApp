from django.contrib import admin
from . import models

# Register your models here.
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'related_league_code', 'player_capacity', )


admin.site.register(models.Tournament, TournamentAdmin)
