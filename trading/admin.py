from django.contrib import admin
from .models import Trade, EtBalance, EtAuthTokens


# Register your models here.


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'is_active', 'sell_currency', 'buy_currency', 'sell_quantity',
                    'buy_quantity', 'create_at', 'updated_at', 'participant', 'type')
    list_display_links = list_display
    list_filter = ['is_active', 'type', 'create_at']


@admin.register(EtBalance)
class EtBalance(admin.ModelAdmin):
    list_display = ('id', 'login', 'balance', 'currency')
    list_display_filter = ['currency']


@admin.register(EtAuthTokens)
class EtAuthTokens(admin.ModelAdmin):
    list_display = ('login', 'token')
