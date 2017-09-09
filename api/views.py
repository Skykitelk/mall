# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse


from api  import permissions
from api.models import *
from api.serializers import *

from rest_framework.permissions import *
from rest_framework.decorators import api_view,parser_classes,permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework_jwt import authentication
#from WXBizDataCrypt import WXBizDataCrypt
import requests
import json

class UserViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny,新建用户通过openId和用户名即可，测试OK
	read: IsAuthenticated,公司内部人员，查看个人信息
	partial_update:IsAuthenticated,管理者和自己，修改个人信息
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = MyUser.objects.all()
	serializer_class = UserSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class AddressViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = Address.objects.all()
	serializer_class = AddressSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class ClassifyViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = Classify.objects.all()
	serializer_class = ClassifySerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]


class GoodsViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class GoodsImageViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = GoodsImage.objects.all()
	serializer_class = GoodsImageSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]


class CartItemViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = CartItem.objects.all()
	serializer_class = CartItemSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class OrderViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = Order.objects.all()
	serializer_class = OrderSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]


class OrderItemViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class PostViewSet(viewsets.ModelViewSet):
	"""
	create: AllowAny
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAdminUser
	list: IsAdminUser
	update: IsAdminUser
	"""
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'create':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]