from django.contrib import admin

from api_backend.models import Participant, ParticipantMatch


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "email"]


admin.site.register(ParticipantMatch)

