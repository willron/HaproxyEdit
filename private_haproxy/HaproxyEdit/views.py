#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
by:willron
'''
__author__ = 'zxp'


from django.shortcuts import render
from django.http import HttpResponse
from models import ACL, ACTION, BACKEND_SERVER


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
haproxycfg_path = '/home/zxp/haproxy.cfg'
haproxycfg_stable = '/home/zxp/桌面/HaproxyEdit/haproxy.cfg.stable.txt'


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
            if not each_backend.server1_name:
                backend_list.append([each_backend.id, each_backend.backend_name, each_backend.server0_name,
                                     each_backend.server0_ip, each_backend.server0_port])
            else:
                backend_list.append([each_backend.id, each_backend.backend_name, each_backend.server0_name,
                                     each_backend.server0_ip, each_backend.server0_port, each_backend.server1_name,
                                     each_backend.server1_ip, each_backend.server1_port])

        return render(request, 'index.html', {'acl': acls_list, 'action': actions_list, 'backend': backend_list})
    else:
        # return HttpResponse('POST')
        post_data = request.POST
        post_all_acl = []
        post_all_action = []
        post_all_backend = []
        with open(haproxycfg_path, 'r') as oldcfg:
            oldcfg = oldcfg.read()
        f = open('haproxy.cfg', 'w')
        for k in post_data:
            if k.startswith('acl'):
                post_all_acl.append(k)
            if k.startswith('action'):
                post_all_action.append(k)
            if k.startswith('backend'):
                post_all_backend.append(k)

        # 处理ACL
        post_all_acl = sorted(post_all_acl)
        all_acl_sorted_list = [post_all_acl[i:i+3] for i in range(0, len(post_all_acl), 3)]
        data_acl = []
        acl_name_check_list = []
        for i in all_acl_sorted_list:
            acl_name_check_list.append(post_data[i[0]])
            if len(i[0].split('_')) < 5:
                data = 'acl {} {} -i {}\n'.format(post_data[i[0]], post_data[i[2]], post_data[i[1]])
            else:
                data = 'acl {} {} -i {}\n'.format(post_data[i[0]], post_data[i[2]], post_data[i[1]])
            data_acl.append(data)

        # 处理BACKEND
        post_all_backend = sorted(post_all_backend)
        all_backend_sorted_list = [post_all_backend[i:i+3] for i in range(0, len(post_all_backend), 3)]
        data_backend = []
        backend_name_check_list = []
        for i in all_backend_sorted_list:
            backend_name_check_list.append(post_data[i[0]])
            if len(i[0].split('_')) < 5:
                data = """backend {}
    balance roundrobin
    option  httpclose
    option  forwardfor
    cookie  SERVERID insert indirect nocache
    server  {}_{}  {}  check  inter	1500  rise 3  fall 3  weight 1\n\n"""\
                    .format(post_data[i[0]], post_data[i[2]],
                            post_data[i[1]].split(':')[0].split('.')[-1], post_data[i[1]])
            else:
                data = """backend {}
    balance roundrobin
    option  httpclose
    option  forwardfor
    cookie  SERVERID insert indirect nocache
    server  {}_{}  {}  check  inter	1500  rise 3  fall 3  weight 1\n\n"""\
                    .format(post_data[i[0]], post_data[i[2]],
                            post_data[i[1]].split(':')[0].split('.')[-1], post_data[i[1]])
            data_backend.append(data)

        # 处理ACTION，同步校验ACL和BACKEND是否存在
        post_all_action = sorted(post_all_action)
        all_action_sorted_list = [post_all_action[i:i+2] for i in range(0, len(post_all_action), 2)]
        data_action = []
        for i in all_action_sorted_list:
            if post_data[i[0]] not in acl_name_check_list:
                return HttpResponse('ACTION中引用了无效的ACL：{}'.format(post_data[i[0]]))
            if post_data[i[1]] not in backend_name_check_list:
                return HttpResponse('ACTION中引用了无效的BACKEND：{}'.format(post_data[i[1]]))

            if len(i[0].split('_')) < 5:
                data = 'use_backend {} if {}\n'.format(post_data[i[1]], post_data[i[0]])
            else:
                data = 'use_backend {} if {}\n'.format(post_data[i[1]], post_data[i[0]])
            data_action.append(data)

        # 文件写入
        with open(haproxycfg_stable, 'r') as cfg_stable:
            # 写入固定数据
            f.write(cfg_stable.read())
            f.write('\n{}\n\n'.format('#'*80))
        f.writelines(data_acl)      # 写入ACL
        f.write('\n{}\n\n'.format('#'*80))
        f.writelines(data_action)     # 写入ACTION
        f.write('\n{}\n\n'.format('#'*80))
        f.writelines(data_backend)
        f.write('\n{}\n\n'.format('#'*80))
        f.close()
        # print sorted(post_all_acl)
        # print sorted(post_all_action)
        # print sorted(post_all_backend)
        return HttpResponse('POST')
