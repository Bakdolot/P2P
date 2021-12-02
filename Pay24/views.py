from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *
from .pay24_services import Pay24ApiRequest


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', ]


class CreatePaymentView(generics.CreateAPIView):
    queryset = Pay24Operation
    serializer_class = CreatePaymentSerializer


class RetrievePaymentView(generics.RetrieveAPIView):
    lookup_field = 'guid'
    queryset = Pay24Operation.objects.all()
    serializer_class = PaymentRetrieveSerializer


class GetCategoriesFromPay24(views.APIView):

    def post(self, request, *args, **kwargs):
        api = Pay24ApiRequest('netex_api', '0265648a8056f0fd290f5ab619e8cd43b21fa68e79ab573b0fc5b881b4f5918t')
        if api.get_all_categories():
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_409_CONFLICT)


class GetServicesFromPay24(views.APIView):
    def post(self, request, *args, **kwargs):
        api = Pay24ApiRequest('netex_api', '0265648a8056f0fd290f5ab619e8cd43b21fa68e79ab573b0fc5b881b4f5918t')
        if api.get_all_services():
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_409_CONFLICT)
