from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters

from .filters import TradeListFilter
from .models import Trade
from .trade_services import checking_and_debiting_balance, get_login, make_transaction
from .serializers import (
    UpdateTradeSerializer, 
    CreateTradeSerializer, 
    RetrieveTradeSerializer
    )
from .permissions import IsOwnerOrReadOnly


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
    queryset = Trade
    serializer_class = UpdateTradeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveTradeSerializer
        return super().get_serializer_class()


class TradeJoinView(generics.GenericAPIView):

    def put(self, request, pk, *args, **kwargs):
        try:
            trade = generics.get_object_or_404(Trade, id=pk)
            login = get_login(request.META.get('HTTP_AUTHORIZATION').split(' ')[1])

            if trade.type == '2':
                trade.participant = login
                trade.save()
                return Response({'status': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)

            elif trade.type == '1':
                if checking_and_debiting_balance(login, trade.buy_quantity, trade.buy_currency):
                    trade.participant = login
                    trade.save()

                    if make_transaction(trade):
                        return Response({'status': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)

            elif trade.type == '3':
                trade.participant = login
                trade.save()
                return Response({'status': 'SUCCESS'}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'reason': 'NOT ENOUGH BALANCE'}, status=status.HTTP_402_PAYMENT_REQUIRED)
