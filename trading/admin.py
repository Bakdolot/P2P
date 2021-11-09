from django.contrib import admin
from .models import TradeCript, TradeCash, EtBalance, EtAuthTokens


# Register your models here.


@admin.register(TradeCript)
class TradeCriptAdmin(admin.ModelAdmin):
    list_display = ('owner', 'is_active', 'sell_currency', 'buy_currency', 'sell_quantity',
                    'buy_quantity', 'create_at', 'updated_at', 'participant')
    list_display_links = list_display
    list_filter = ['is_active', 'create_at']


@admin.register(TradeCash)
class TradeCashAdmin(admin.ModelAdmin):
    list_display = ('owner', 'is_active', 'sell_currency', 'buy_currency', 'sell_quantity',
                    'buy_quantity', 'create_at', 'updated_at', 'participant')
    list_display_links = list_display
    list_filter = ['is_active', 'create_at']


@admin.register(EtBalance)
class EtBalance(admin.ModelAdmin):
    list_display = ('login', 'balance', 'currency')
    list_display_filter = ['currency']


@admin.register(EtAuthTokens)
class EtAuthTokens(admin.ModelAdmin):
    list_display = ('login', 'token')
