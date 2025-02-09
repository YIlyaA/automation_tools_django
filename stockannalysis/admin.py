from django.contrib import admin
from .models import Stock

class StockAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol", "sector", "exchange", "country"]
    search_fields = ["name", "symbol", "exchange"]

admin.site.register(Stock, StockAdmin)
