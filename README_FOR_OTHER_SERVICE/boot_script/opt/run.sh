#! /bin/bash

net_dev=`ip address|grep "2: eth"|awk '{print $2}'|tr -d ":"`
ifconfig eth0 &>/dev/null
if [ "$?" != "0" ];then
    /bin/cp /etc/sysconfig/network-scripts/ifcfg-eth0 /etc/sysconfig/network-scripts/ifcfg-${net_dev}
    /bin/sed -i "s/eth0/${net_dev}/" /etc/sysconfig/network-scripts/ifcfg-${net_dev}
    service network restart
    sleep 3
fi

ifconfig ${net_dev} &>/dev/null
if [ "$?" == "0" ];then
    localip=`ifconfig|grep "inet "|grep Bcast|awk -F'[ :]+' '{print $4}'`
    
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.com.zone
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.com.cn.zone
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.net.zone
    /bin/sed -i "s/\(\*.*\)192\.168\..*/\1${localip}/" /var/named/hk515.cn.zone
    /bin/sed -r -i "/haproxyedit_server_local/s/(192\.168\.0\.[0-9]\{1,3\}|127\.0\.0\.1)/${localip}/" /usr/local/haproxy/etc/haproxy.cfg
    /bin/sed -r -i "/haproxyedit_server_local/s/(192\.168\.0\.[0-9]\{1,3\}|127\.0\.0\.1)/${localip}/" /var/www/HaproxyEdit/haproxy.cfg.stable.end.txt
fi

/etc/init.d/named start
/etc/init.d/haproxy start
cd /var/www/HaproxyEdit;nohup /usr/bin/python manage.py runserver ${localip}:8000 &
