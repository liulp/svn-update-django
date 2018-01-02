# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import User
from django.views.decorators.csrf import csrf_exempt
import json


def signin(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'signin.html', context)

@csrf_exempt
def checked(request):   #js 登陆 链接
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = User.objects.filter(username__exact=username,password__exact=password)
    if user:
        request.session['username'] = username
        request.session.set_expiry(3600)
        url = request.session.get('pre_url', '/') #url 为登陆前访问的页面
        if url == '/accounts/logout/':
            url = '/'
        else:
             url = url
        return HttpResponse(json.dumps('{"result":"%s"}') % url )
    else:
        return HttpResponse(json.dumps('{"result":400}'))#用户名密码错误


def login_required(func):
    def _deco(request, *args, **kwargs):
        request.session['pre_url'] = request.get_full_path()  # 用来验证登陆返回原来的页面，对应login 函数
        username = request.session.get('username', '')
        if not username:
            return HttpResponseRedirect(reverse('login:signin',args=()))
        request.session['username'] = username
        request.session.set_expiry(3600)
        response = func(request, *args, **kwargs)
        return response
    return _deco

def login_required_ajax(func):
    def _deco(request, *args, **kwargs):
        request.session['pre_url'] = request.get_full_path()  # 用来验证登陆返回原来的页面，对应login 函数
        username = request.session.get('username', '')
        if not username:
            return HttpResponse(json.dumps('{"result":400}'))
        request.session['username'] = username
        request.session.set_expiry(3600)
        response = func(request, *args, **kwargs)
        return response
    return _deco