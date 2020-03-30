from django.contrib import admin
from .models import Question, TeamProfile, Answer

# Register your models here.
admin.site.register(Question)
# admin.site.register(TeamProfile)
# admin.site.register(Answer)


class AnswersInline(admin.TabularInline):
    model = Answer


@admin.register(TeamProfile)
class TeamProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'jokers', 'current_question')
    inlines = [AnswersInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('team', 'question', 'result', 'time')
