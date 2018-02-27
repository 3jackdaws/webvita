from rest_framework.views import APIView, Request, Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app.models import Resume, ResumeObject
from app.settings import BASE_DIR
import json

import re

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class ObjectSerializer(ModelSerializer):
    class Meta:
        model = ResumeObject
        fields = (
            'id',
            'type',
            'data'
        )

class ResumeSerializer(ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            'id',
            'name',
            'owner',
            'archived',
            'theme',
            'layout',
            'script',
        )

    # def update(self, instance, validated_data):
    #     if 'name' in validated_data:
    #         instance.name = validated_data.pop('name')
    #
    #     if 'archived' in validated_data:
    #         instance.archived = validated_data.pop('archived') == 'true'
    #
    #     layout = validated_data.get('layout')
    #     if layout:
    #         if 'id' in layout:
    #             instance.layout_id =
    #
    #     theme = validated_data.get('theme')
    #
    #     script = validated_data.get('script')
    #     return instance

class ResumeView(APIView):

    http_user = True

    def get(self, request, id):
        try:
            resume = Resume.objects.get(id=id)
        except:
            return Response(status=404)
        return Response(ResumeSerializer(resume).data)

    def post(self, request, _):
        name = request.POST.get('name', 'New Resume')
        resume = Resume(name=name, owner=request.user)

        with open(BASE_DIR + '/templates/app/resumes/default_resume.html') as fp:
            resume.layout = ResumeObject.objects.create(
                type='layout',
                owner=request.user,
                data=json.dumps({
                    'name':'Custom Layout for Resume',
                    'text':fp.read()
                })
            )

        resume.theme = ResumeObject.objects.create(
            type='theme',
            owner=request.user,
            data=json.dumps({
                'name':'Custom Theme for Resume',
                'text':''
            })
        )
        resume.script = ResumeObject.objects.create(
            type='script',
            owner=request.user,
            data=json.dumps({
                'name':'Custom Script for Resume',
                'text':''
            })
        )

        resume.save()
        return Response(ResumeSerializer(resume).data)

    def put(self, request:Request, id):
        user_resumes = Resume.objects.filter(owner=request.user)
        data = json.loads(request.POST.get('payload', '{}'))
        try:
            resume = user_resumes.get(id=id)
        except:
            return Response(status=404)

        serializer = ResumeSerializer(resume)

        print(json.dumps(data, indent=2))

        # for attr in ['layout_id', 'theme_id', 'script_id']:
        #     if request.data.get(attr) == resume.__getattribute__(attr):
        #         request.data.pop(attr)

        resume = serializer.update(resume, data)

        return Response(ResumeSerializer(resume).data)





class ObjectsView(APIView):
    http_user = True

    def get(self, request, id=None):
        type = request.GET.get('type')
        group = ResumeObject.objects.filter(owner=request.user)
        if type:
            group = group.filter(type=type)

        if id:
            print('here')
            try:
                object = group.get(id=id)
                return Response(ObjectSerializer(object).data)
            except:
                return Response(status=404)

        else:
            return Response([ObjectSerializer(o).data for o in group])

    def post(self, request, _):
        print(request.data)
        object = ObjectSerializer(data=request.data)
        if object.is_valid():
            data = object.validated_data
            data['owner'] = request.user
            object = object.create(data)
            return Response(ObjectSerializer(object).data)
        else:
            return Response(object.errors)

    def put(self, request, id):
        print(request.data)
        group = ResumeObject.objects.filter(owner=request.user)
        obj = group.get(id=id)
        if not obj:
            return Response(status=403)

        serializer = ObjectSerializer(obj)
        obj = serializer.update(obj, request.data)
        return Response(ResumeObject(obj).data)

    def delete(self, request, id):
        group = ResumeObject.objects.filter(owner=request.user)
        try:
            object = group.get(id=id)
            object.delete()
            return Response(status=200)
        except:
            return Response(status=404)

