from django.urls import path
from .views import *


urlpatterns = [
    path('category/list/', CategoryListView.as_view()),
    path('service/list/', ServiceListView.as_view()),
    path('create/', CreatePaymentView.as_view()),
    path('get/<str:guid>/', RetrievePaymentView.as_view())
]