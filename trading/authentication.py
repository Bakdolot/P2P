from rest_framework import authentication
from rest_framework import exceptions

from .models import EtUsers, EtAuthTokens


class TradeAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        try:
            login = EtAuthTokens.objects.get(token=token.split(' ')[1]).login
            user = EtUsers.objects.get(login=login)
        except EtUsers.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        except:
            raise exceptions.AuthenticationFailed('Incorrect authentication token')

        return (user, None)