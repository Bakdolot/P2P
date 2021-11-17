from django.urls import path
from .views import *


urlpatterns = [
    path('create/', CreateTransferView.as_view()),
    path('get/<int:pk>/', GetTransferView.as_view()),
    path('get/list/', GetTransferListView.as_view()),
    path('accept/<int:pk>/', AcceptTransferView.as_view())
]
