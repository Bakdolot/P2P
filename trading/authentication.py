from rest_framework import authentication
from rest_framework import exceptions

from .models import EtUsers, EtAuthTokens
from datetime import datetime
import base64


class TradeAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        try:
            base64_bytes = token.split(' ')[1].encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            token = message_bytes.decode('ascii')
            token_obj = EtAuthTokens.objects.get(token=token)
            token_exp = datetime.fromtimestamp(int(token_obj.date_expiration))
            if datetime.now() > token_exp:
                raise exceptions.AuthenticationFailed('Срок действия данного токена истек')
            user = EtUsers.objects.get(login=token_obj.login)
        except EtUsers.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь не найден')
        except EtAuthTokens.DoesNotExist:
            raise exceptions.AuthenticationFailed('Данный токен не найден')

        return (user, None)