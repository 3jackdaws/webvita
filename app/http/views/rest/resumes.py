from rest_framework.views import APIView, Request, Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app.models import Resume, ResumeLayout, ResumeTheme, ResumeField, ResumeScript

import re

from rest_framework.serializers import ModelSerializer

class ResumeSerializer(ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            'id',
            'name',
            'fields',
            'theme',
            'layout',
            'scripts'
        )



class FieldSerializer(ModelSerializer):
    class Meta:
        model = ResumeField
        fields = (
            ''
        )


class ResumeView(APIView):

    http_user = True

    def get(self, request, id):
        try:
            resume = Resume.objects.get(id=id)
        except:
            return Response(status=404)
        return Response(ResumeSerializer(instance=resume).data)

    def post(self, request, _):
        name = request.POST.get('name')
        print(request.user, type(request.user))
        resume = Resume.objects.create(name=name, owner=request.user)
        return Response(ResumeSerializer(instance=resume).data)

    def put(self, request:Request, id):
        try:
            resume = Resume.objects.get(id=id)
        except:
            return Response(status=404)

        print(request.data)
        resume = ResumeSerializer(resume, request.data)
        resume.update(resume, request.data)
        return Response(resume.data)



