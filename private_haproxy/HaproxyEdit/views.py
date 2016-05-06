#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
by:willron
'''
__author__ = 'zxp'


import os
import shutil
import commands
from django.shortcuts import render
from django.http import HttpResponse
from models import ACL, ACTION, BACKEND_SERVER



# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
haproxycfg_path = '/home/zhengxupeng/zxp/haproxy.cfg'
haproxycfg_stable = 'haproxy.cfg.stable.txt'

reload_haproxy_cmd = 'ls ~'

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

        for k in post_data:
            if k.startswith('acl'):
                post_all_acl.append(k)
            if k.startswith('action'):
                post_all_action.append(k)
            if k.startswith('backend'):
                post_all_backend.append(k)

        # 处理ACL
        post_all_acl = sorted(post_all_acl)     # 排序，将同一ID的数据放一起
        all_acl_sorted_list = [post_all_acl[i:i+3] for i in range(0, len(post_all_acl), 3)]     # 将同一ID的数据分段
        data_acl = []       # 存放即将放入配置文件的配置语句
        acl_name_check_list = []    # 存放acl名称，供后面做校验
        data_acl_id = []        # 存放post过来的acl数据的id值
        acl_sql = []        # 存放即将写入DB的sql语句
        # print all_acl_sorted_list
        for i in all_acl_sorted_list:
            sql = {}
            acl_name_check_list.append(post_data[i[0]])
            # if len(i[0].split('_')) < 5:
            #     get_acl_id = int(i[0].split('_')[1])
            # else:
            #     # 新增的数据
            #     get_acl_id = int(i[0].split('_')[1])
            get_acl_id = int(i[0].split('_')[1])

            data = 'acl {} {} -i {}\n'.format(post_data[i[0]], post_data[i[2]], post_data[i[1]])

            sql['acl_name'] = post_data[i[0]]
            sql['mode'] = post_data[i[2]]
            sql['defined'] = post_data[i[1]]
            sql['id'] = get_acl_id

            data_acl.append(data)
            data_acl_id.append(get_acl_id)
            acl_sql.append(sql)

        # 处理BACKEND
        post_all_backend = sorted(post_all_backend)
        all_backend_sorted_list = [post_all_backend[i:i+3] for i in range(0, len(post_all_backend), 3)]
        data_backend = []
        backend_name_check_list = []
        data_backend_id = []
        backend_sql = []
        # print all_backend_sorted_list
        for i in all_backend_sorted_list:
            sql = {}
            backend_name_check_list.append(post_data[i[0]])
    #         if len(i[0].split('_')) < 5:
    #             data = """backend {}
    # balance roundrobin
    # option  httpclose
    # option  forwardfor
    # cookie  SERVERID insert indirect nocache
    # server  {}_{}  {}  check  inter	1500  rise 3  fall 3  weight 1\n\n"""\
    #                 .format(post_data[i[0]], post_data[i[2]],
    #                         post_data[i[1]].split(':')[0].split('.')[-1], post_data[i[1]])
    #             get_backend_id = int(i[0].split('_')[1])
    #
    #         else:
            data = """backend {}
balance roundrobin
option  httpclose
option  forwardfor
cookie  SERVERID insert indirect nocache
server  {}_{}  {}  check  inter	1500  rise 3  fall 3  weight 1\n\n"""\
                .format(post_data[i[0]], post_data[i[2]],
                        post_data[i[1]].split(':')[0].split('.')[-1], post_data[i[1]])

            get_backend_id = int(i[0].split('_')[1])

            sql['backend_name'] = post_data[i[0]]
            sql['server0_name'] = post_data[i[2]]
            sql['server0_ip'] = post_data[i[1]].split(':')[0]
            sql['server0_port'] = post_data[i[1]].split(':')[1]
            sql['id'] = get_backend_id

            data_backend.append(data)
            data_backend_id.append(get_backend_id)
            backend_sql.append(sql)

        # 处理ACTION，同步校验ACL和BACKEND是否存在
        post_all_action = sorted(post_all_action)
        all_action_sorted_list = [post_all_action[i:i+2] for i in range(0, len(post_all_action), 2)]
        data_action = []
        data_action_id = []
        action_sql = []
        # print all_action_sorted_list
        for i in all_action_sorted_list:
            sql = {}
            if post_data[i[0]] not in acl_name_check_list:
                return HttpResponse('ACTION中引用了无效的ACL：{}'.format(post_data[i[0]]))
            if post_data[i[1]] not in backend_name_check_list:
                return HttpResponse('ACTION中引用了无效的BACKEND：{}'.format(post_data[i[1]]))

            # if len(i[0].split('_')) < 5:
            #     data = 'use_backend {} if {}\n'.format(post_data[i[1]], post_data[i[0]])
            #     get_action_id = int(i[0].split('_')[1])
            # else:

            data = 'use_backend {} if {}\n'.format(post_data[i[1]], post_data[i[0]])

            get_action_id = int(i[0].split('_')[1])

            sql['acl_name'] = post_data[i[0]]
            sql['backend_name'] = post_data[i[1]]
            sql['id'] = get_action_id

            data_action.append(data)
            data_action_id.append(get_action_id)
            action_sql.append(sql)

        # 读取旧文件留存。如果重启haproxy失败则恢复
        with open(haproxycfg_path, 'r') as oldcfg:
            oldcfg = oldcfg.read()

        f = open('haproxy.cfg', 'w')

        # 文件写入
        with open(haproxycfg_stable, 'r') as cfg_stable:
            # 写入固定数据
            f.write(cfg_stable.read())
            f.write('\n{}\n\n'.format('#'*80))
        f.writelines(data_acl)      # 写入ACL
        f.write('\n{}\n\n'.format('#'*80))
        f.writelines(data_action)     # 写入ACTION
        f.write('\n{}\n\n'.format('#'*80))
        f.writelines(data_backend)      # 写入BACKEND
        f.write('\n{}\n\n'.format('#'*80))
        f.close()

        shutil.copyfile('haproxy.cfg', haproxycfg_path)     # 复制新的配置文件到haproxy文件夹里
        reloadhaproxy = commands.getstatusoutput(reload_haproxy_cmd)
        if reloadhaproxy[0] != 0:
            with open(haproxycfg_path, 'w') as rollback:
                rollback.write(oldcfg)
            return HttpResponse(reloadhaproxy[1])
        else:
        # haproxy重启成功，将数据写入数据库

        # 处理ACL

            # 删除数据
            all_old_id_acl = [i['id'] for i in ACL.objects.all().values('id')]
            del_id_acl = set(all_old_id_acl) - set(data_acl_id)
            if len(del_id_acl) > 0:
                for i in del_id_acl:
                    ACL.objects.get(id=i).delete()

            # 添加和修改数据
            for each_acl_sql in acl_sql:
                sql_acl_id = each_acl_sql['id']
                each_acl_sql.pop('id')
                obj, create = ACL.objects.update_or_create(id=sql_acl_id, defaults=each_acl_sql)
                # print obj.__dict__
                # print create

        # 处理BACKEND
            # 删除数据
            all_old_id_backend = [i['id'] for i in BACKEND_SERVER.objects.all().values('id')]
            del_id_backend = set(all_old_id_backend) - set(data_backend_id)
            if len(del_id_backend) > 0:
                for i in del_id_backend:
                    BACKEND_SERVER.objects.get(id=i).delete()
            # 添加和修改数据
            for each_backend_sql in backend_sql:
                sql_backend_id = each_backend_sql['id']
                each_backend_sql.pop('id')
                obj, create = BACKEND_SERVER.objects.update_or_create(id=sql_backend_id, defaults=each_backend_sql)
                # print obj.__dict__
                # print create


        # 处理ACTION
            # 删除数据
            all_old_id_action = [i['id'] for i in ACTION.objects.all().values('id')]
            del_id_action = set(all_old_id_action) - set(data_action_id)
            if len(del_id_action) > 0:
                for i in del_id_action:
                    ACTION.objects.get(id=i).delete()
            # 添加和修改数据
            for each_action_sql in action_sql:
                sql_action_id = each_action_sql['id']
                each_action_sql.pop('id')
                obj, create = ACTION.objects.update_or_create(id=sql_action_id, defaults=each_action_sql)
                # print obj.__dict__
                # print create

        return HttpResponse('POST')
