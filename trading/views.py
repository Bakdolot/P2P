from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters

from .filters import TradeListFilter
from .models import Trade
from .trade_services import (
    get_create_data, make_transaction, 
    send_notification, trade_update
)
from internal_transfer.services import balance_transfer, check_user_balance
from .serializers import (
    UpdateTradeSerializer,
    CreateTradeSerializer,
    RetrieveTradeSerializer,
    AcceptCardPaymentTradeSerializer
)
from .permissions import IsOwnerOrReadOnly, IsOwner, IsParticipant, IsNotOwner


class TradeListView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TradeListFilter
    queryset = Trade.objects.filter(is_active=True, status='expectation')
    serializer_class = RetrieveTradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade
    serializer_class = CreateTradeSerializer

    def create(self, request, *args, **kwargs):
        data = get_create_data(request)
        if data['data_status']:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class TradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade.objects.filter(is_active=True, status='expectation')
    serializer_class = UpdateTradeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveTradeSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        trade = generics.get_object_or_404(Trade, id=self.kwargs.get('pk'))
        try:
            if self.request.user.login == trade.owner: 
                return Trade.objects.all()
        except AttributeError:
            None
        return super().get_queryset()
    
    def delete(self, request, *args, **kwargs):
        trade = self.get_object()
        balance_transfer(trade.owner, trade.sell_currency, trade.sell_quantity, is_plus=True)
        return super().delete(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        trade = self.get_object()
        if trade_update(request, trade):
            return super().put(request, *args, **kwargs)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)
    
    def patch(self, request, *args, **kwargs):
        trade = self.get_object()
        if trade_update(request, trade):
            return super().patch(request, *args, **kwargs)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class AcceptCardReceivedPaymentTradeView(generics.GenericAPIView):
    queryset = Trade.objects.filter(type='card', status='process', participant_sent=False)
    permission_classes = [IsOwner]
    
    def put(self, request, *args, **kwargs):
        trade = self.get_object()
        make_transaction(trade)
        trade.owner_confirm = True
        trade.save()
        return Response(
            {'status': 'Trade was completed successfully'},
            status=status.HTTP_202_ACCEPTED)


class TradeJoinView(generics.GenericAPIView):
    queryset = Trade.objects.filter(status='expectation', is_active=True)
    permission_classes = [IsNotOwner]

    def put(self, request, *args, **kwargs):
        trade = self.get_object()
        login = request.user.login
        if trade.type == 'cash' or trade.type == 'card':
            trade.participant = login
            trade.status = 'process'
            trade.save()
            return Response({'status': 'SUCCESS JOIN'}, status=status.HTTP_202_ACCEPTED)
        elif trade.type == 'cript':
            if check_user_balance(login, trade.sell_currency, trade.sell_quantity):
                trade.participant = login
                make_transaction(trade)
                return Response({'status': 'SUCCESS TRADE WAS COMPLETED'}, status=status.HTTP_202_ACCEPTED)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)


class AcceptTradeView(generics.GenericAPIView):  # Наличка
    permission_classes = [IsOwner]
    queryset = Trade.objects.filter(is_active=True, status='process', type='cash')

    def put(self, request, *args, **kwargs):
        trade = self.get_object()
        make_transaction(trade)
        return Response(
            {'status': 'Trade was completed successfully'},
            status=status.HTTP_202_ACCEPTED)


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
            trade.status = 'expectation'
            trade.save()
            return Response({'participant': 'quited'}, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
