#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
by:willron
'''
__author__ = 'zxp'

from django.db import models


class ACL(models.Model):
	acl_name = models.CharField(max_length=99)
	mode = models.CharField(max_length=20)
	defined = models.CharField(max_length=255)


class ACTION(models.Model):
	backend_name = models.CharField(max_length=99)
	acl_name = models.CharField(max_length=99)
	# backend_name = models.ForeignKey(BACKEND_SERVER, related_name='GOTO')
	# acl_name = models.ForeignKey(ACL, related_name='IF')


class BACKEND_SERVER(models.Model):
	backend_name = models.CharField(max_length=99)
	server0_name = models.CharField(max_length=99)
	server0_ip = models.GenericIPAddressField()
	server0_port = models.IntegerField()
	server1_name = models.CharField(max_length=99, null=True)
	server1_ip = models.GenericIPAddressField(null=True)
	server1_port = models.IntegerField(null=True)








