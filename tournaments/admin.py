from django.contrib import admin
from .models import Tournament, TournamentParticipant

class TournamentParticipantInline(admin.TabularInline):
    model = TournamentParticipant
    extra = 0

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')  # ОК, можно тут использовать метод
    list_filter = ('start_date', 'end_date')  # ❌ убрали is_active отсюда
    search_fields = ('title', 'description')
    inlines = [TournamentParticipantInline]

    def is_active(self, obj):
        return obj.is_active()
    
    is_active.boolean = True
