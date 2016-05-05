#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
by:willron
'''
__author__ = 'zxp'


from django.shortcuts import render
from django.http import HttpResponse
from models import ACL, ACTION, BACKEND_SERVER


didi = []


def index(request):
    if request.method == 'GET':

        all_acl = ACL.objects.all()
        all_action = ACTION.objects.all()
        all_backend = BACKEND_SERVER.objects.all()

        acls_list = []
        actions_list = []
        backend_list = []

        for each_acl in all_acl:
            acls_list.append([each_acl.id, each_acl.acl_name, each_acl.mode, each_acl.defined])

        for each_action in all_action:
            actions_list.append([each_action.id, each_action.backend_name, each_action.acl_name])

        for each_backend in all_backend:
            if each_backend.server1_name == None:
                backend_list.append([each_backend.id, each_backend.backend_name, each_backend.server0_name,
                                     each_backend.server0_ip, each_backend.server0_port])
            else:
                backend_list.append([each_backend.id, each_backend.backend_name, each_backend.server0_name,
                                     each_backend.server0_ip, each_backend.server0_port, each_backend.server1_name,
                                     each_backend.server1_ip, each_backend.server1_port])

        return render(request, 'index.html', {'acl': acls_list, 'action':actions_list, 'backend':backend_list})
    else:
        # return HttpResponse('POST')
        post_data = request.POST
        post_all_acl = []
        post_all_action = []
        post_all_backend = []
        for k in post_data:
            if k.startswith('acl'):
                post_all_acl.append(k)
            if k.startswith('action'):
                post_all_action.append(k)
            if k.startswith('backend'):
                post_all_backend.append(k)
        print sorted(post_all_acl)
        print sorted(post_all_action)
        print sorted(post_all_backend)
        return HttpResponse('POST')