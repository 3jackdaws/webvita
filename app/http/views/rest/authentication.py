from rest_framework.views import APIView, Request, Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'groups')


# /api/sessions
class SessionView(APIView):

    def get(self, request: Request):
        user = request.user  # type: User
        if user.is_anonymous:
            return Response(status=403)
        else:
            return Response(UserSerializer(instance=user).data)

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username, password)
        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return Response(UserSerializer(instance=user).data)
            else:
                return Response(status=401)

    def delete(self, request):
        logout(request)
        return Response(status=200)
