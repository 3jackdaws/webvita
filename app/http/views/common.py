import mimetypes

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Resume, ResumeObject
from rest_framework.views import APIView
from rest_framework.response import Response


from app.settings import STATIC_BASE, BASE_DIR
from django.contrib.auth import login, authenticate, logout


def index(request):
    user = request.user  # type: User
    if user.is_anonymous:
        return redirect('/login/')
    return render(request, 'app/index.html')


def render_user_login(request):
    return render(request, 'app/accounts/login.html')

def render_user_register(request):
    return render(request, 'app/accounts/registration.html')

def render_resumes(request):
    if request.user.is_anonymous:
        return redirect('/login/')
    user_resumes = Resume.objects.filter(owner=request.user).filter(archived=False)
    context = {
        'resumes':user_resumes
    }
    return render(request, 'app/resumes/list.html', context)

def render_single_resume(request, resume_id):
    if request.user.is_anonymous:
        return redirect('/login/')
    resume = Resume.objects.filter(owner=request.user).get(id=resume_id)
    print(resume.owner)

    if not resume:
        return redirect('/')
    context = {
        'resume': resume,
        'title':resume.name,
    }
    return render(request, 'app/resumes/single2.html', context)


def static(request, path):
    filepath = STATIC_BASE + path
    with open(filepath, 'rb') as fp:
        sometext = fp.read()
    return FileResponse(sometext, content_type=mimetypes.guess_type(filepath)[0])

def public_link_resume(request, token):
    print(token)
    try:
        resume = Resume.objects.get(sharelink=token)
    except Exception as e:
        print(e)
        return redirect('/')
    return render(request, 'app/resumes/public.html', {'resume':resume})


def search_user_attributes(request):
    import json
    results = set()
    query = request.GET.get('skill').lower()
    if query:
        prefilter = ResumeObject.objects.filter(type='skills')
        for obj in prefilter:
            data = json.loads(obj.data)
            if query in data['skill'].lower():
                results.add(obj.owner)
        return Response([
            f'/r/{x.first_name}-{x.last_name}' for x in results
        ])
    else:
        return Response({})

class PublicSearchView(APIView):

    def get(self, request):
        import json
        type = request.GET.get('type').lower()
        query = request.GET.get('q').lower()
        result_set = set()
        if query:
            prefilter = ResumeObject.objects.filter(type=type)
            for obj in prefilter:
                if query in obj.data:
                    result_set.add(obj.owner)

        return Response([
            f'/r/{x.first_name}-{x.last_name}'.lower() for x in result_set
        ])