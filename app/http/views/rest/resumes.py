from rest_framework.views import APIView, Request, Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from app.models import Resume, ResumeLayout, ResumeTheme, ResumeField, ResumeScript, Skill, Education
from app.settings import BASE_DIR

import re

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class LayoutSerializer(ModelSerializer):
    class Meta:
        model = ResumeLayout
        fields = (
            'name',
            'markup'
        )
class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            'id',
            'name',
        )

class SkillView(APIView):

    http_user = True

    def get(self, request, id):
        try:
            skill = Skill.objects.filter(owner=request.user).get(id=id)
        except:
            return Response(status=404)
        return Response(SkillSerializer(instance=skill).data)

    def post(self, request, _):
        if 'skill' not in request.data:
            return Response(status=404)

        skill = Skill.objects.create(name=request.data['skill'], owner=request.user)

        return Response(SkillSerializer(skill).data)


class EducationSerializer(ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'id',
            'school',
            'degree',
            'date',
        )

class EducationView(APIView):

    http_user = True

    def get(self, request, id):
        try:
            edu = Education.objects.filter(owner=request.user).get(id=id)
        except:
            return Response(status=404)
        return Response(EducationSerializer(edu).data)

    def post(self, request, _):
        school = request.data.get('school')
        degree = request.data.get('degree')
        date = request.data.get('date')

        if not (school and degree and date):
            print('WANT school, degree, date, got: ', dict(request.data))
            return Response(status=400)

        education = Education.objects.create(
            school=school,
            degree=degree,
            date=date,
            owner=request.user
        )

        return Response(EducationSerializer(education).data)


class ResumeSerializer(ModelSerializer):
    layout = LayoutSerializer()
    class Meta:
        model = Resume
        fields = (
            'id',
            'name',
            'fields',
            'theme',
            'layout',
            'script'
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
        resume = Resume(name=name, owner=request.user)

        with open(BASE_DIR + '/templates/app/resumes/default_resume.html') as fp:
            resume.layout = ResumeLayout.objects.create(name=f'Custom Layout for {resume.name}', owner=request.user, markup=fp.read())

        resume.theme = ResumeTheme.objects.create(name=f'Custom Theme for {resume.name}', owner=request.user)

        resume.script = ResumeScript.objects.create(name=f'Custom Script for {resume.name}', owner=request.user)

        resume.save()
        return Response(ResumeSerializer(instance=resume).data)

    def put(self, request:Request, id):
        try:
            resume = Resume.objects.get(id=id)
        except:
            return Response(status=404)


        print(request.data)
        if "layout" in request.data:
            resume.layout.markup = request.data['layout']
            resume.layout.save()

        if "theme" in request.data:
            resume.theme.stylesheet = request.data['theme']
            resume.theme.save()

        if "script" in request.data:
            resume.script.text = request.data['script']
            resume.script.save()

        resume.save()


        return Response(ResumeSerializer(resume).data)



class AttributesView(APIView):

    http_user = True

    def get(self, request):
        user = request.user
        attributes = {
            'basics':[
                {'tag':'fullname', 'value':f'{user.first_name} {user.last_name}'},
                {'tag':'email', 'value':f'{user.email}'},
            ],
            'skills':[SkillSerializer(skill).data for skill in Skill.objects.filter(owner=request.user)],
            'education':[EducationSerializer(edu).data for edu in Education.objects.filter(owner=request.user)]
        }
        return Response(attributes)