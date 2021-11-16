from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from django.http import Http404

from .models import InternalTransfer
from .services import get_data, transfer_data, check_recipient
from .serializers import CreateTransferSerializer, GetTransferSerializer, UpdateTransferSerializer
from trading.permissions import IsNotOwner
from .permissions import IsOwnerOrRecipient, IsNotOwner


class CreateTransferView(generics.CreateAPIView):
    serializer_class = CreateTransferSerializer
    queryset = InternalTransfer

    def create(self, request, *args, **kwargs):
        data = request.data
        if not check_recipient(data.get('recipient'), data.get('currency')):
            return Response({'message': 'Recipient with this login does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        data = get_data(request)
        if data['status']:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'message': 'Not enough money'}, status=status.HTTP_400_BAD_REQUEST)


class GetTransferListView(generics.ListAPIView):
    serializer_class = GetTransferSerializer

    def get_queryset(self):
        try:
            login = self.request.user.login
            queryset = InternalTransfer.objects.filter(owner=login).union(InternalTransfer.objects.filter(recipient=login))
            return queryset
        except AttributeError:
            raise Http404


class GetTransferView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GetTransferSerializer
    queryset = InternalTransfer.objects.all()
    permission_classes = [IsNotOwner, IsOwnerOrRecipient]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return super().get_serializer_class()
        return UpdateTransferSerializer

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return super().get_queryset()
        return InternalTransfer.objects.filter(status=False)


class AcceptTransferView(generics.GenericAPIView):
    queryset = InternalTransfer.objects.filter(status=False)
    permission_classes = [IsNotOwner]

    def post(self, request, *args, **kwargs):
        transfer = self.get_object()
        if transfer.security_code == request.data.get('security_code'):
            if transfer_data(transfer):
                return Response({'msg': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
