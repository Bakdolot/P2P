from decimal import Decimal
from django.http import request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from django.db import transaction

from .filters import TradeListFilter
from .models import EtBalance, Trade
from .trade_services import (
    checking_and_debiting_balance,
    make_transaction, send_notification,
    get_commission_value, delete_trade
)
from .serializers import (
    UpdateTradeSerializer,
    CreateTradeSerializer,
    RetrieveTradeSerializer,
    AcceptCardPaymentTradeSerializer
)
from .utils import get_commission
from .permissions import IsOwnerOrReadOnly, IsOwner, IsParticipant, IsStarted, IsNotOwner


class TradeListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TradeListFilter
    queryset = Trade.objects.filter(is_active=True, status='expectation')
    serializer_class = RetrieveTradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade
    serializer_class = CreateTradeSerializer

    def create(self, request, *args, **kwargs):
        login = request.user.login
        data = request.POST.copy()
        with transaction.atomic():
            if checking_and_debiting_balance(login, data['sell_quantity'], data['sell_currency']):

                data['owner'] = login

                data['sell_quantity_with_commission'] = get_commission(int(data.get('sell_quantity')), get_commission_value())
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class TradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade.objects.filter(is_active=True, status='expectation')
    serializer_class = UpdateTradeSerializer
    permission_classes = [IsOwnerOrReadOnly, IsStarted]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveTradeSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        trade = generics.get_object_or_404(Trade, id=self.kwargs.get('pk'))
        try:
            if self.request.user.login == trade.owner: 
                return Trade.objects.all()
            return super().get_queryset()
        except AttributeError:
            return super().get_queryset()
    
    def delete(self, request, *args, **kwargs):
        trade = self.get_object()
        if delete_trade(trade):
            return super().delete(request, *args, **kwargs)
        return Response({'error': 'FAILED TO DELETE'}, status=status.HTTP_400_BAD_REQUEST)


class AcceptCardReceivedPaymentTradeView(generics.GenericAPIView):
    queryset = Trade.objects.filter(type='card', status='process', participant_sent=False)
    permission_classes = [IsOwner]
    
    def put(self, request, *args, **kwargs):
        trade = self.get_object()
        if make_transaction(trade):
            trade.owner_confirm = True
            trade.save()
            return Response(
                {'status': 'Trade was completed successfully'},
                status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_202_ACCEPTED)


class TradeJoinView(generics.GenericAPIView):
    queryset = Trade.objects.filter(status='expectation', is_active=True)
    permission_classes = [IsNotOwner]

    def put(self, request, *args, **kwargs):

        trade = self.get_object()
        login = request.user.login

        if trade.type == 'cash':
            trade.participant = login
            trade.status = 'process'
            trade.save()
            return Response({'status': 'SUCCESS JOIN'}, status=status.HTTP_202_ACCEPTED)

        elif trade.type == 'cript':
            if checking_and_debiting_balance(login, trade.buy_quantity, trade.buy_currency):
                trade.participant = login
                if make_transaction(trade):
                    return Response({'status': 'SUCCESS TRADE WAS COMPLETED'}, status=status.HTTP_202_ACCEPTED)

        elif trade.type == 'card':
            trade.participant = login
            trade.status = 'process'
            trade.save()
            return Response({'status': 'SUCCESS JOIN'}, status=status.HTTP_202_ACCEPTED)

        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class AcceptTradeView(generics.GenericAPIView):  # Наличка
    permission_classes = [IsOwner]
    queryset = Trade.objects.filter(is_active=True, status='process', type='cash')

    def put(self, request, *args, **kwargs):
        with transaction.atomic():
            trade = self.get_object()
            user = EtBalance.objects.get(login=trade.participant, currency=trade.sell_currency)
            user.balance = str(Decimal(user.balance) + Decimal(trade.sell_quantity))
            trade.status = 'finished'
            trade.save()
            user.save()
            return Response({'status': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)


class AcceptCardSentPaymentTradeView(generics.RetrieveUpdateAPIView):  # Карта
    queryset = Trade.objects.filter(is_active=True, type='card', participant_sent=False)
    serializer_class = AcceptCardPaymentTradeSerializer
    permission_classes = [IsParticipant]

    def put(self, request, *args, **kwargs):
        if super().put(request, *args, **kwargs):
            trade = self.get_object()
            trade.participant_sent = True
            trade.save()
            send_notification(trade.owner)
            return Response({'participant': 'sent'}, status=status.HTTP_202_ACCEPTED)


class TradeQuitView(generics.GenericAPIView):
    permission_classes = [IsParticipant]
    queryset = Trade.objects.filter(status='process')

    def put(self, request, *args, **kwargs):
        trade = self.get_object()
        if trade.type == 'cash' or (trade.type == 'card' and not trade.participant_sent):
            trade.participant_sent = None
            trade.status = 'expectation'
            trade.save()
            return Response({'participant': 'quited'}, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

