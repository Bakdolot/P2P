from django.urls import path
from .views import TradeListView, TradeCreateView, TradeUpdate


urlpatterns = [
    path('', TradeListView.as_view()),
    path('create/', TradeCreateView.as_view()),
    path('retrieve_update_delete/<int:pk>/', TradeUpdate.as_view())
]