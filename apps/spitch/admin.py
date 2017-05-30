from django.contrib import admin
from .models import Spitch


@admin.register(Spitch)
class SpitchAdmin(admin.ModelAdmin):
    list_display = ('user', 'ask', 'active')

