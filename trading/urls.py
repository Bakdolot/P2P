from django.urls import path
from .views import (
    TradeJoinView, TradeListView,
    TradeCreateView, TradeUpdateView,
    AcceptTradeView,
    AcceptCardSentPaymentTradeView,
    AcceptCardReceivedPaymentTradeView,
    TradeQuitView,
    MyTradeListView,
    CommissionView
    )


urlpatterns = [
    # path('', Hello.as_view()),
    path('', TradeListView.as_view()),
    path('my_trades/', MyTradeListView.as_view()),
    path('create/', TradeCreateView.as_view()),
    path('join/<int:pk>/', TradeJoinView.as_view()),
    path('retrieve_update_delete/<int:pk>/', TradeUpdateView.as_view()),
    path('trade/accept/<int:pk>/', AcceptTradeView.as_view()),
    path('accept_payment/sent/<int:pk>/', AcceptCardSentPaymentTradeView.as_view()),
    path('accept_payment/get/<int:pk>/', AcceptCardReceivedPaymentTradeView.as_view()),
    path('quit/<int:pk>/', TradeQuitView.as_view()),
    path('commission/', CommissionView.as_view()),
]