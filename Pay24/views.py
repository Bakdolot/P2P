from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category',]


class CreatePaymentView(generics.CreateAPIView):
    queryset = Pay24Operation
    serializer_class = CreatePaymentSerializer


class RetrievePaymentView(generics.RetrieveAPIView):
    lookup_field = 'guid'
    queryset = Pay24Operation.objects.all()
    serializer_class = PaymentRetrieveSerializer
