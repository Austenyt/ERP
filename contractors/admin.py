from django.contrib import admin

from contractors.models import Contractor


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    list_filter = []
    search_fields = ['code', 'name']
    ordering = ['code']
