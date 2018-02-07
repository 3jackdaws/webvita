"""ott URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.views.static import serve
from rest_framework.authtoken.views import obtain_auth_token

from app.http.views import common
from app.http.views.rest.authentication import SessionView
from app.http.views.rest.accounts import AccountView
from app.http.views.rest.resumes import ResumeView, SkillView, EducationView



urlpatterns = [
    # USER PAGE URLS

    url(r'^$', common.render_resumes),

    url(r'^login/$', common.render_user_login),
    url(r'^register/$', common.render_user_register),
    url(r'^resumes/$', common.render_resumes),
    url(r'^resumes/([0-9]+)/$', common.render_single_resume),
    url(r'^render-resume/([0-9]+)/$', common.super_safe_resume_renderer),



    # USER LOGIN/LOGOUT
    url(r'^api/sessions', SessionView.as_view()),
    url(r'^api/account', AccountView.as_view()),




    url(r'^api/resumes/([0-9]+)?', ResumeView.as_view()),
    url(r'^api/skills/([0-9]+)?', SkillView.as_view()),
    url(r'^api/education/([0-9]+)?', EducationView.as_view()),







    # EVERYTHING ELSE TO HOME
    url(r'.*', lambda x: HttpResponseRedirect('/')),
]
