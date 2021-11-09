from django.urls import path
from .views import TradeCriptJoinView, TradeListView, TradeCreateView, TradeCriptUpdateView, TradeCashUpdateView, TradeCashJoinView


urlpatterns = [
    path('', TradeListView.as_view()),
    path('create/', TradeCreateView.as_view()),
    path('join/cript/<int:pk>/', TradeCriptJoinView.as_view()),
    path('join/cash/<int:pk>/', TradeCashJoinView.as_view()),
    path('retrieve_update_delete/cript/<int:pk>/', TradeCriptUpdateView.as_view()),
    path('retrieve_update_delete/cash/<int:pk>/', TradeCashUpdateView.as_view()),
]