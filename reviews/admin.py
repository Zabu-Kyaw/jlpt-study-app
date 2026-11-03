from django.contrib import admin

from .models import Answer, Review


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "card", "is_correct", "answered_at")
    list_filter = ("is_correct", "user")
    ordering = ("-answered_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "card", "due_at", "interval_days", "repetitions")