# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from login.models import User
from login.views import login_required, login_required_ajax
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json, paramiko, re, os,multiprocessing, subprocess, datetime, pytz
from update_api import  Linux, Windows
from ftplib import FTP
from django.shortcuts import render
from models import Project, Host,  Entry, Rollback
# Create your views here.


def upload(prohost,xiangmu,svn_path,src_path,back_dir):
    if prohost.host.type == 'L':
        L = Linux(prohost.host.ip, prohost.host.name, prohost.host.password, prohost.host.port)
        L.sftp_connect()
        L.ssh_connect()
        for local_dir in xiangmu:
            local_dir = local_dir.replace(svn_path,src_path)
            remote_dir = local_dir.replace(src_path,prohost.dest_path)
            backup_dir = os.path.split(local_dir.replace(src_path,back_dir).rstrip('/'))[0]
            if os.path.exists(local_dir):
                if os.path.isfile(local_dir):
                    dest_dir = os.path.split(remote_dir)[0]
                    # backup_dir = os.path.split(backup_dir)[0]
                    try:
                        L.sftp.stat(dest_dir)
                        CMD = "mkdir -p %s  && cp -p %s %s" % (backup_dir, remote_dir, backup_dir)
                        L.ssh_cmd(CMD)
                    except:
                        CMD = "mkdir -p %s" % dest_dir
                        L.ssh_cmd(CMD)
                    L.sftp.put(local_dir, remote_dir)
                    print "upload %s to remote %s" % (local_dir, remote_dir)
                elif os.path.isdir(local_dir):
                    try:
                        L.sftp.stat(remote_dir)
                        CMD = "mkdir -p %s  && cp -rfp %s %s" % (backup_dir, remote_dir, backup_dir)
                        L.ssh_cmd(CMD)
                    except:
                        CMD = "mkdir -p %s" % remote_dir
                        L.ssh_cmd(CMD)
                    L.upload_dir(local_dir,remote_dir)
            else:
                print "##### update erro#####"
        L.close()
    elif prohost.host.type == 'W':
        W = Windows(prohost.host.ip, prohost.host.name, prohost.host.password, prohost.host.port)
        for local_dir in xiangmu:
            W.ftp_connect()
            local_dir = local_dir.replace(svn_path, src_path)
            remotedir = local_dir.replace(src_path, prohost.dest_path)
            #backup_dir = os.path.split(local_dir.replace(svn_path, back_dir))[0]
            if os.path.isfile(local_dir):
                remotedir = os.path.split(remotedir)[0]
                remotefile = os.path.split(local_dir)[1]
                try:
                    W.ftp.mkd(remotedir)
                except:
                    pass
                W.ftp.cwd(remotedir)
                W.upload_file(local_dir, remotefile)
            elif os.path.isdir(local_dir):
                try:
                    W.ftp.mkd(remotedir)
                except:
                    pass
                W.ftp.cwd(remotedir)
                W.upload_files(local_dir, remotedir)
            else:
                print "##### update erro#####"
            W.ftp_close()
    else:
        pass


@csrf_exempt
@login_required_ajax
def roll_back(request):#回滚
    username = request.session.get('username','')
    user = User.objects.get(username__exact=username)
    var3 = request.POST.get('var3', '')
    entry = Entry.objects.get(id=var3)
    item = entry.item
    time = entry.date
    program = entry.project.program
    svn_path = entry.project.svn_path
    src_path = entry.project.src_path
    time_path = (time + datetime.timedelta(hours=8)).strftime('%Y%m%d%H%M')
    backup_dir = os.path.join('/opt/backup', program, time_path).replace('\\', '/')
    back_dir = item.replace(svn_path,backup_dir)
    try:
        rollback = Rollback()
        rollback.date = time
        rollback.item = item
        rollback.project = entry.project
        rollback.user = user
        rollback.rolldate = timezone.now()
        rollback.save()
        for prohost in  Project.objects.get(program=program).prohost_set.all():
            if prohost.host.type == 'L':
                local_dir = item.replace(svn_path, src_path)
                remote_dir = item.replace(svn_path, prohost.dest_path)
                if os.path.isdir(local_dir):
                    remote_dir = os.path.split(remote_dir.rstrip('/'))[0]
                L = Linux(prohost.host.ip, prohost.host.name, prohost.host.password, prohost.host.port)
                L.ssh_connect()
                CMD = "\\cp -rfp %s %s" % (back_dir, remote_dir)
                L.ssh_cmd(CMD)
                L.close()
    except:
        HttpResponse(json.dumps('{"result":400}'))
    return HttpResponse(json.dumps('{"result":200}'))


@csrf_exempt
@login_required_ajax
def content(request):   #js 上传文件
    username = request.session.get('username', '')
    user = User.objects.get(username__exact=username)
    content = request.POST.get('content', '')
    xm_path = {}
    xm_item = {}
    pro_path = []

    for pro in Project.objects.all():
        xm_path[pro.program] = tuple(pro.propath.split())
        pro_path.extend((str(pro.propath).split()))
        xm_item[pro.program] = []

    for item in content.split('\n'):
        if item:
            try:
                item_url = item.split()[2].replace('\\', '/').strip()
            except:
                item_url = item.replace('\\', '/').strip()
            if not item_url.startswith(tuple(pro_path)):
                return HttpResponse(json.dumps('{"result":401, "item":\"%s\","path":\"%s\"}' % (item, pro_path)))
            if str(item_url).rstrip('/') in pro_path:
                return HttpResponse(json.dumps('{"result":404, "item":\"%s\"}' % item))
            for key in xm_path:
                try:
                    if item_url.startswith(xm_path[key][0]):
                        xm_item[key].append(item_url)
                    elif item_url.startswith(xm_path[key][1]):
                        item_url = os.path.split(Project.objects.get(program=key).svn_path)[0] + item_url
                        xm_item[key].append(item_url)
                except:
                    pass

    for key in xm_item:
        if xm_item[key]:
            p = Project.objects.get(program=key)
            src_path = p.src_path.replace('\\','/')
            svn_path = p.svn_path
            for item in xm_item[key]:
                local_dir = item.replace(svn_path, src_path)
                if not os.path.exists(local_dir):
                    return HttpResponse(json.dumps('{"result":402, "item":\"%s\"}' % local_dir))

            time = timezone.now()
            time_path = (time + datetime.timedelta(hours=8)).strftime('%Y%m%d%H%M')
            back_dir = os.path.join('/opt/backup', key, time_path).replace('\\', '/')

            for item in xm_item[key]:
                entry = Entry()
                entry.user = user
                entry.item = item
                entry.date = time
                entry.project = Project.objects.get(program=key)
                entry.save()

            for prohost in p.prohost_set.all():
                try:
                    upload(prohost, xm_item[key], svn_path, src_path, back_dir)
                except:
                    return HttpResponse(json.dumps('{"result":403}'))
    return HttpResponse(json.dumps('{"result":200}'))

