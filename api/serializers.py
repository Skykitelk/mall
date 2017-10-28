#!/venv/bin/env python
# -*- coding: utf-8 -*-
#copyRight by yangguozhanzhao
#序列化数据库的查询结果到json，rest_framwork最方便的地方

from rest_framework import serializers
from api.models import *

class ClassifySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Classify
		fields = ('url','id','name')

class GoodsImageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GoodsImage
		fields = ('url','id','goods','image')


class GoodsSerializer(serializers.HyperlinkedModelSerializer):
	image=GoodsImageSerializer(many=True,read_only=True)
	class Meta:
		model = Goods
		fields = ('url','id','types','name','mainImage','price','image')

class SwiperSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Swiper
		fields = ('url','id','title','goods','image')

class AddressSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Address
		fields = ('url','id','name','address','tel','is_def','user')

class CartItemSerializer(serializers.HyperlinkedModelSerializer):
	goods_detail = GoodsSerializer(source='goods', read_only=True)

	class Meta:
		model = CartItem
		fields = ('url','id','goods_detail','goods','count','user','selected')

				
class UserSerializer(serializers.HyperlinkedModelSerializer):
	address = AddressSerializer(many=True, read_only=True)
	cart_user = CartItemSerializer(many=True,read_only=True)
	class Meta:
		model = MyUser
		# 直接在fields里面写related_name即可
		fields = ('url','id','openId', 'name','gender','avatar','address','cart_user')

	def create(self, validated_data):
		user = MyUser(
			openId=validated_data['openId'],
		)
		user.set_password("1234pttk")
		user.save()
		return user


class OrderSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Order
		fields = ('url','id','number','user','state','price','recipientName','recipientTel','recipientAddress','create_at')

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
	goods_detail = GoodsSerializer(source='goods', read_only=True)
	class Meta:
		model = OrderItem
		fields = ('url','id','goods','order','goods_count','goods_name','goods_price','goods_detail')


class PostSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Post
		fields = ('url','id','order','post_company','post_number')				

class MyOrderSerializer(serializers.HyperlinkedModelSerializer):
	order_item=OrderItemSerializer(many=True,read_only=True)
	class Meta:
		model = Order
		fields = ('url','id','number','user','state','price','recipientName','recipientTel','recipientAddress','create_at','order_item','post_order')



		