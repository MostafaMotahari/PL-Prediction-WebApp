from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', )

admin.site.register(User, UserAdmin)