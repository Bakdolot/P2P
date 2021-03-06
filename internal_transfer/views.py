from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from trading.utils import convert_unixtime_to_datetime
from trading.models import EtParameters
from .models import InternalTransfer
from .services import transfer_data, balance_transfer
from .serializers import CreateTransferSerializer, GetTransferSerializer, UpdateTransferSerializer
from .permissions import IsOwnerOrRecipient, IsRecipient, IsUntoHimself


class CreateTransferView(generics.CreateAPIView):
    serializer_class = CreateTransferSerializer
    queryset = InternalTransfer
    permission_classes = [IsUntoHimself]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetTransferListView(generics.ListAPIView):
    serializer_class = GetTransferSerializer

    def get_queryset(self):
        try:
            login = self.request.user.login
            if self.request.GET.get('my'):
                queryset = InternalTransfer.objects.filter(owner=login)
            elif self.request.GET.get('me'):
                queryset = InternalTransfer.objects.filter(recipient=login)
            else:
                queryset = InternalTransfer.objects.filter(owner=login).union(InternalTransfer.objects.filter(recipient=login))
            for i in range(len(queryset)):
                queryset[i].create_at = convert_unixtime_to_datetime(queryset[i].create_at)
            return queryset
        except AttributeError:
            raise Http404


class GetTransferView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GetTransferSerializer
    queryset = InternalTransfer.objects.all()
    permission_classes = [IsOwnerOrRecipient]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return super().get_serializer_class()
        return UpdateTransferSerializer

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return super().get_queryset()
        return InternalTransfer.objects.filter(status=False)

    def get_object(self):
        object = super().get_object()
        if self.request.method in SAFE_METHODS:
            object.create_at = convert_unixtime_to_datetime(object.create_at)
        return object
        
    def delete(self, request, *args, **kwargs):
        transfer = self.get_object()
        balance_transfer(transfer.owner, transfer.currency, transfer.sum, is_plus=True)
        return super().delete(request, *args, **kwargs)


class AcceptTransferView(generics.GenericAPIView):
    queryset = InternalTransfer.objects.filter(status=False)
    permission_classes = [IsRecipient]

    def post(self, request, *args, **kwargs):
        transfer = self.get_object()
        if transfer.security_code == str(request.data.get('security_code')):
            if transfer_data(transfer):
                return Response({'detail': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)
        return Response({'detail': '???????????????? ?????? ??????????????????'}, status=status.HTTP_400_BAD_REQUEST)


class CommissionInternalTransferView(generics.GenericAPIView):

    def get(self, request):
        commission = EtParameters.objects.get(id=69)
        return Response({'commission': commission.value}, status=status.HTTP_200_OK)


class QuantityInternalTransfersView(generics.GenericAPIView):

    def get(self, request):
        quantity = InternalTransfer.objects.filter(recipient=request.user.login, status=False).count()
        return Response({'quantity': quantity}, status=status.HTTP_200_OK)
