from django.urls import path
from .views import *


urlpatterns = [
    path('category/list/', CategoryListView.as_view()),
    path('service/list/', ServiceListView.as_view()),
    path('pay/', CreatePaymentView.as_view()),
    path('get/<str:guid>/', RetrievePaymentView.as_view()),
    path('get_categories/', GetCategoriesFromPay24.as_view()),
    path('get_services/', GetServicesFromPay24.as_view()),
    path('get/list/', ListPaymentView.as_view()),
]
