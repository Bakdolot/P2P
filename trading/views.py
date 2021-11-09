from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from django.http import QueryDict

from .filters import TradeListFilter
from .models import Trade, EtAuthTokens
from .trade_services import checking_and_debiting_balance, get_login, make_transaction
from .serializers import UpdateTradeSerializer, CreateTradeSerializer, TradeJoinSerializer

import json

class TradeListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TradeListFilter
    queryset = Trade.objects.filter(is_active=True)
    serializer_class = CreateTradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade

    serializer_class = CreateTradeSerializer

    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        login = get_login(token)
        data = request.POST.copy()
        if checking_and_debiting_balance(login, data['sell_quantity'], data['sell_currency']):
            data['owner'] = login

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class TradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade.objects.all()
    serializer_class = UpdateTradeSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CreateTradeSerializer
        return super().get_serializer_class()

    def put(self, request, *args, **kwargs):
        try:
            login = get_login(request.META.get('HTTP_AUTHORIZATION').split(' ')[1])
            if request.data['owner'] == login:

                return super().update(request, *args, **kwargs)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TradeJoinView(generics.UpdateAPIView):
    serializer_class = TradeJoinSerializer
    queryset = Trade

    def update(self, request, pk, *args, **kwargs):
        trade = generics.get_object_or_404(Trade, id=pk)
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        login = get_login(token)
        if checking_and_debiting_balance(login, trade.buy_quantity, trade.buy_currency):
            data = request.data.copy()
            data['participant'] = login
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if trade.type == '1':
                make_transaction(trade)
            return Response(serializer.data)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)
