from django.contrib import admin
from .models import Trade
# Register your models here.


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'is_active', 'sell', 'buy', 'sell_quantity',
                    'buy_quantity', 'create_at', 'updated_at', 'participant', 'type')
    list_display_links = list_display
    list_filter = ['is_active', 'type', 'create_at']


