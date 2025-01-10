from django.contrib import admin
from .models import Currency, Vacancy


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('date', 'BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL')
    list_filter = ('date',)
    search_fields = ('date',)
    list_per_page = 20

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key_skills', 'salary', 'area_name', 'published_at')
    list_filter = ('published_at',)
    search_fields = ('published_at',)
    list_per_page = 20