from django.contrib import admin
from .models import Trade, EtBalance, EtAuthTokens, EtParameters


# Register your models here.

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'owner', 'sell_currency', 'buy_currency', 'sell_quantity',
                    'buy_quantity', 'create_at', 'updated_at', 'participant')
    list_display_links = list_display
    list_filter = ['create_at', 'type', 'status']


@admin.register(EtBalance)
class EtBalance(admin.ModelAdmin):
    list_display = ('id', 'login', 'balance', 'currency')
    list_display_filter = ['currency']


@admin.register(EtAuthTokens)
class EtAuthTokens(admin.ModelAdmin):
    list_display = ('login', 'token')


@admin.register(EtParameters)
class EtParametersAdmin(admin.ModelAdmin):
    list_display = ('id', 'categories', 'name', 'alias', 'value', 'sort')
