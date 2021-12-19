from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import InternalTransfer
from trading.models import EtOperations
from .services import (
    check_min_sum, 
    check_user_balance, 
    balance_transfer, 
    get_finance, 
    create_operation, 
    get_commission, 
    get_client_ip,
    get_correct_sum
    )


class TransferValidationMixin:
    def __init__(self, instance=None, data=..., **kwargs):
        data._mutable = True
        data['sum'] = get_correct_sum(data['currency'], data['sum'])
        data._mutable = False
        super().__init__(instance=instance, data=data, **kwargs)

    def validate(self, attrs):
        data = super().validate(attrs)
        if not check_min_sum(data.get('sum'), data.get('currency'), 'internal'): 
            raise serializers.ValidationError({'detail': 'Сумма меньше минимальной суммы'})
        if check_user_balance(data.get('owner'), data.get('currency'), data.get('sum')):
            raise serializers.ValidationError({'detail': 'Не достаточно средств'})
        return data


class CreateTransferSerializer(TransferValidationMixin, serializers.ModelSerializer):
    security_code = serializers.CharField(validators=[RegexValidator('^[0-9]{6,10}$', message='Пароль должен быть менее 10 символов и больше 6 символов и содержать только цифры', code='invalid_code')])
    recipient = serializers.EmailField()
    owner = serializers.EmailField(required=False)

    class Meta:
        model = InternalTransfer
        fields = ['owner', 'currency', 'sum', 'recipient', 'security_code']

    def create(self, validated_data):
        user = self.context.get('request').user.login
        validated_data['owner'] = user
        obj = super().create(validated_data)
        ip = get_client_ip(self.context.get('request'))
        balance_transfer(user, obj.currency, obj.sum, is_plus=False)
        currecy_alias = get_finance(obj.currency).alias
        operation_id = create_operation(
            'transfer', user, currecy_alias, 
            obj.currency, obj.sum, 
            ip, transfer_type='credit', 
            requisite=obj.recipient,
            commission=get_commission('internal_transfer')
            )
        obj.owner_operation = operation_id
        obj.save()
        return obj


class GetTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalTransfer
        exclude = [
            'security_code',
            'owner_operation',
            'recipient_operation'
        ]


class UpdateTransferSerializer(TransferValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = InternalTransfer
        fields= ['currency', 'sum', 'recipient', 'security_code']


    def update(self, instance, validated_data):
        if instance.sum != validated_data.get('sum') or instance.currency != validated_data.get('currency'):
            balance_transfer(instance.owner, instance.currency, instance.sum, is_plus=True)
            balance_transfer(instance.owner, validated_data.get('currency'), validated_data.get('sum'), is_plus=False)
            operation = EtOperations.objects.get(operation_id=instance.owner_operation)
            operation.currency = validated_data.get('currency')
            operation.sum = validated_data.get('sum')
            operation.save()
        return super().update(instance, validated_data)
