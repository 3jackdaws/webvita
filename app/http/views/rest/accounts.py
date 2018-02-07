from rest_framework.views import APIView, Request, Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
import re

from rest_framework.serializers import ModelSerializer


EMAIL_REGEX = r'.+@.+[.].+'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'groups')


# /api/sessions
class AccountView(APIView):

    def get(self, request: Request):
        user = request.user  # type: User
        if user.is_anonymous:
            return Response(status=403)
        else:
            return Response(UserSerializer(instance=user).data)

    def post(self, request):
        username =          request.POST.get('email')
        password =          request.POST.get('password')
        first_name =        request.POST.get('first_name')
        last_name =        request.POST.get('last_name')
        context = {}

        if not username or not re.findall(EMAIL_REGEX, username):
            return Response({'message':'Must provide a valid email.'}, status=400)

        if not password:
            return Response({'message':'Must provide a password'}, status=400)
        try:
            user = User.objects.get(username=username)
            return Response({'message':'Email already used.'}, status=400)
        except:
            pass
        user = User.objects.create(username=username, email=username, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return Response(UserSerializer(instance=user).data)
