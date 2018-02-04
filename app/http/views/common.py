import mimetypes

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Resume


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
        'title':resume.name
    }
    return render(request, 'app/resumes/single.html', context)

def super_safe_resume_renderer(request, id):
    resume = Resume.objects.filter(owner=request.user).get(id=id)
    context = {
        'resume':resume
    }
    return render(request, 'app/resumes/ultra_mega_safe_resume_template.html', context)

def static(request, path):
    filepath = STATIC_BASE + path
    with open(filepath, 'rb') as fp:
        sometext = fp.read()
    return FileResponse(sometext, content_type=mimetypes.guess_type(filepath)[0])
