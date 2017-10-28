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
import random
import string
import hashlib
import xml.etree.ElementTree as ET
import time
# linptech
APPID="wx4809d29bf7ddd03e"
APPSECRET="236b7032f04d2fe918ebb24a7f722728"

MCHID="1489626502"
APIKEY="linptech87413985linptech87413985"


# code换取openId登录
@api_view(['POST'])
def login(request,format=None):
	code=request.data['code']
	#print code
	#code -> openid
	keyURL= 'https://api.weixin.qq.com/sns/jscode2session?appid='+APPID+'&secret='+APPSECRET+'&js_code='+code+'&grant_type=authorization_code'
	r = requests.post(keyURL).json()
	#print "r:",r

	openId= r['openid']	
	user = MyUser.objects.filter(openId=openId)
	if user:
		pass
	else:
		userSerializer=UserSerializer()
		data={
				"openId":openId,
			}
		userSerializer.create(data)

	user = MyUser.objects.get(openId=openId)
	serializer = UserSerializer(user,context={'request': request})
	#print type(serializer.data)
	return Response(serializer.data)


def dict_to_xml(dict_data):
	xml = ["<xml>"]
	for k, v in dict_data.iteritems():
		xml.append("<{0}>{1}</{0}>".format(k, v))
	xml.append("</xml>")
	return "".join(xml)


def xml_to_dict(xml_data):
	xml_dict = {}
	root = ET.fromstring(xml_data)
	for child in root:
		xml_dict[child.tag] = child.text
	return xml_dict

# 微信支付：统一下单
@api_view(['POST'])
def unifiedorder(request,format=None):

	# 构造order
	order={
		"appid":APPID,
		"mch_id":MCHID,
		"device_info":"WEB",
		"nonce_str":''.join(random.sample(string.ascii_letters + string.digits, 32)),
		"body":request.data['body'],
		"out_trade_no":request.data['out_trade_no'], #订单号
		"total_fee":request.data['total_fee'],
		"spbill_create_ip":"47.93.103.136",  #服务器ip
		"notify_url":"http://127.0.0.1:8000/api/paynotify",
		"trade_type":"JSAPI",
		"openid":request.data['openid'],
	}
	stringA = '&'.join(["{0}={1}".format(k, order.get(k))for k in sorted(order)])
	stringSignTemp = '{0}&key={1}'.format(stringA, APIKEY)
	# print stringSignTemp
	order["sign"]=hashlib.md5(stringSignTemp.encode("utf8")).hexdigest()
	# print dict_to_xml(order)
	returnInfo=requests.post(url="https://api.mch.weixin.qq.com/pay/unifiedorder",data=dict_to_xml(order).encode("utf8"),headers={'Content-Type': 'application/xml'})
	data = xml_to_dict(returnInfo.content)
	paySignData = {
		'appId': APPID,
		'timeStamp': str(round(time.time())),
		'nonceStr': data["nonce_str"],
		'package': 'prepay_id={0}'.format(data["prepay_id"]),
		'signType': 'MD5'
		}
	stringB = '&'.join(["{0}={1}".format(k, paySignData.get(k))for k in sorted(paySignData)])
	stringSignTempB = '{0}&key={1}'.format(stringB, APIKEY)
	paySignData['sign']=hashlib.md5(stringSignTempB.encode("utf8")).hexdigest()
	return JsonResponse(paySignData)

#个人订单查询
@api_view(["GET"])
def myOrder(request,format=None):
	# myorders=[]
	# orders=Order.objects.filter(user=request.user.id)
	# for order in orders:
	# 	serializer = OrderSerializer(order,context={'request': request})
	# 	myorders.append(serializer.data)
	# return JsonResponse(myorders,safe=False)
	myorders=[]
	orders=Order.objects.filter(user=request.user.id).prefetch_related('order_item')
	for order in orders:
		serializer = MyOrderSerializer(order,context={'request': request})
		myorders.append(serializer.data)
	return JsonResponse(myorders,safe=False)






## list／create／retrieve／update／partial_update／destroy

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
					#'partial_update':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class AddressViewSet(viewsets.ModelViewSet):
	"""
	create: IsAuthenticated
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAuthenticated
	list: IsAuthenticated
	update: IsAuthenticated
	本身应该是IsOnwer
	"""
	queryset = Address.objects.all()
	serializer_class = AddressSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class ClassifyViewSet(viewsets.ModelViewSet):
	"""
	create: IsAdminUser
	read: AllowAny
	partial_update:IsAdminUser
	delete: IsAdminUser
	list: AllowAny
	update: IsAdminUser
	"""
	queryset = Classify.objects.all()
	serializer_class = ClassifySerializer

	# permission 管理
	permission_classes=[IsAdminUser, ]
	permissionByAction = {'read':[AllowAny,],
							'list':[AllowAny,],
							}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]


class GoodsViewSet(viewsets.ModelViewSet):
	"""
	create: IsAdminUser
	read: AllowAny
	partial_update:IsAdminUser
	delete: IsAdminUser
	list: AllowAny
	update: IsAdminUser
	"""
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer

	# permission 管理
	permission_classes=[IsAdminUser, ]
	permissionByAction = {'retrieve':[AllowAny,],
						'list':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class GoodsImageViewSet(viewsets.ModelViewSet):
	"""
	create: IsAdminUser
	read: AllowAny
	partial_update:IsAdminUser
	delete: IsAdminUser
	list: AllowAny
	update: IsAdminUser
	"""
	queryset = GoodsImage.objects.all()
	serializer_class = GoodsImageSerializer

	# permission 管理
	permission_classes=[IsAdminUser, ]
	permissionByAction = {'retrieve':[AllowAny,],
							'list':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]


class SwiperViewSet(viewsets.ModelViewSet):
	"""
	create: IsAdminUser
	read: AllowAny
	partial_update:IsAdminUser
	delete: IsAdminUser
	list: AllowAny
	update: IsAdminUser
	"""
	queryset = Swiper.objects.all()
	serializer_class = SwiperSerializer

	# permission 管理
	permission_classes=[IsAdminUser, ]
	permissionByAction = {'retrieve':[AllowAny,],
						'list':[AllowAny,],
						}
	def get_permissions(self):
		try:
			return [permission() for permission in self.permissionByAction[self.action]]
		except KeyError: 
			return [permission() for permission in self.permission_classes]

class CartItemViewSet(viewsets.ModelViewSet):
	"""
	create: IsAuthenticated
	read: IsAuthenticated
	partial_update:IsAuthenticated
	delete: IsAuthenticated
	list: IsAdminUser
	update: IsAuthenticated
	"""
	queryset = CartItem.objects.all()
	serializer_class = CartItemSerializer

	# permission 管理
	permission_classes=[IsAuthenticated, ]
	permissionByAction = {'list':[IsAdminUser,],
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