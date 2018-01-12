import mimetypes

from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


from app.settings import STATIC_BASE, BASE_DIR
from django.contrib.auth import login, authenticate, logout


def index(request):
    user = request.user  # type: User
    if user.is_anonymous:
        return redirect('/login/')
    return render(request, 'app/index.html')


def render_user_login(request):
    return render(request, 'app/accounts/login.html')

def static(request, path):
    filepath = STATIC_BASE + path
    with open(filepath, 'rb') as fp:
        sometext = fp.read()
    return FileResponse(sometext, content_type=mimetypes.guess_type(filepath)[0])
