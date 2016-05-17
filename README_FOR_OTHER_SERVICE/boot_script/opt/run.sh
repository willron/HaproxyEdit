#! /bin/bash

# 检查eth0是否存在。在VMWARE导入镜像后，会重置网卡，所以系统进入后eth0会消失，重置后的新网卡一般命名为eth1
ifconfig eth0 &>/dev/null

# 如果eth0不否在，则复制eth0配置信息到新网卡，然后修改并重启网络
if [ "$?" != "0" ];then
    net_dev=`ip address|grep "2: eth"|awk '{print $2}'|tr -d ":"`
    /bin/cp /etc/sysconfig/network-scripts/ifcfg-eth0 /etc/sysconfig/network-scripts/ifcfg-${net_dev}
    /bin/sed -i "s/eth0/${net_dev}/" /etc/sysconfig/network-scripts/ifcfg-${net_dev}
fi
service network restart

# 检查新网卡是否生效
ifconfig ${net_dev} &>/dev/null
if [ "$?" == "0" ];then
	# 新网卡生效则获取其IP（网卡配置为DHCP自动获取IP）
    localip=`ifconfig|grep "inet "|grep Bcast|awk -F'[ :]+' '{print $4}'`
    # 修改DNS服务解析配置文件，将公司域名指向自身服务器
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.com.zone
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.com.cn.zone
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.net.zone
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.cn.zone
	# 修改初始的haproxy配置文件，将HaproxyEdit项目后端IP地址修改为自身服务器IP，解决头一次开机访问haproxyedit.hk515.com出现503错误
    /bin/sed -i "/haproxyedit_server_local/s/192\.168\.0\.[0-9]\{1,3\}/${localip}/" /usr/local/haproxy/etc/haproxy.cfg
	# 修改固定的HaproxyEdit项目后端IP地址。
    /bin/sed -i "/haproxyedit_server_local/s/192\.168\.0\.[0-9]\{1,3\}/${localip}/" /var/www/HaproxyEdit/haproxy.cfg.stable.end.txt
fi
# 启动DNS域名解析服务
/etc/init.d/named start
# 启动haproxy服务
/etc/init.d/haproxy start
# 启动HaproxyEdit项目（django）
cd /var/www/HaproxyEdit;nohup /usr/bin/python manage.py runserver ${localip}:8000 &
