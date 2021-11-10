from django.urls import path
from .views import TradeJoinView, TradeListView, TradeCreateView, TradeUpdateView


urlpatterns = [
    path('', TradeListView.as_view()),
    path('create/', TradeCreateView.as_view()),
    path('join/<int:pk>/', TradeJoinView.as_view()),
    path('retrieve_update_delete/<int:pk>/', TradeUpdateView.as_view()),
]