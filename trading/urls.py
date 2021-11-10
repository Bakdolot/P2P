from django.urls import path
from .views import (
    TradeJoinView, TradeListView,
    TradeCreateView, TradeUpdateView,
    AcceptTradeView,
    AcceptCardPaymentTradeView
                    )


urlpatterns = [
    path('', TradeListView.as_view()),
    path('create/', TradeCreateView.as_view()),
    path('join/<int:pk>/', TradeJoinView.as_view()),
    path('retrieve_update_delete/<int:pk>/', TradeUpdateView.as_view()),
    path('trade/accept/<int:pk>/', AcceptTradeView.as_view()),
    path('accept_payment/<int:pk>/', AcceptCardPaymentTradeView.as_view()),
]