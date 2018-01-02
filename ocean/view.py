# -*- coding: utf-8 -*-

# from django.http import HttpResponse
from django.shortcuts import render
from login.views import login_required
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from update.models import Entry, Rollback
import datetime


def Pages(request):
    ONE_PAGE_OF_DATA = 10
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
        curPageR = int(request.GET.get('curPageR', '1'))
        allPageR = int(request.GET.get('allPageR', '1'))
        pageTypeR = str(request.GET.get('pageTypeR', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
        curPageR = 1
        allPageR = 1
        pageTypeR = ''

        # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    if pageTypeR == 'pageDownR':
        curPageR += 1
    elif pageTypeR == 'pageUpR':
        curPageR -= 1

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    entrys = Entry.objects.all().order_by('-id')[startPos:endPos]
    startPosR = (curPageR - 1) * ONE_PAGE_OF_DATA
    endPosR = startPosR + ONE_PAGE_OF_DATA
    rollbacks = Rollback.objects.all().order_by('-id')[startPosR:endPosR]

    if curPageR == 1 and allPageR == 1:  # 标记1
        allPostCountsR = Rollback.objects.count()
        allPageR = allPostCountsR // ONE_PAGE_OF_DATA
        remainPostR = allPostCountsR % ONE_PAGE_OF_DATA
        if remainPostR > 0:
            allPageR += 1
        elif allPageR == 0 and remainPostR == 0:
            allPageR = 1

    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = Entry.objects.count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
        elif allPage == 0 and remainPost == 0:
            allPage = 1
    return entrys,  curPage, allPage, rollbacks,  curPageR, allPageR



@login_required
def index(request):
    entrys, curPage, allPage, rollbacks,  curPageR, allPageR = Pages(request)
    return render_to_response('index.html', {'entrys': entrys, 'allPage': allPage, 'curPage': curPage, 'rollbacks': rollbacks, 'allPageR': allPageR, 'curPageR': curPageR})