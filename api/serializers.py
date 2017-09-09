#!/venv/bin/env python
# -*- coding: utf-8 -*-
#copyRight by yangguozhanzhao
#序列化数据库的查询结果到json，rest_framwork最方便的地方

from rest_framework import serializers
from api.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = MyUser
		fields = ('url','id','openId', 'name','gender','avatar')
	
	def create(self, validated_data):
		user = MyUser(
			name=validated_data['name'],
			openId=validated_data['openId'],
			gender=validated_data['gender'],
		)
		user.set_password("1234pttk")
		user.save()
		return user

class AddressSerializer(serializers.HyperlinkedModelSerializer):
	user=serializers.HyperlinkedRelatedField(read_only=True,view_name='address_user')
	class Meta:
		model = Address
		fields = ('url','id','name','address','tel','is_def','user')

class ClassifySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Classify
		fields = ('url','id','name')


class GoodsSerializer(serializers.HyperlinkedModelSerializer):
	types=serializers.HyperlinkedRelatedField(read_only=True,view_name='goods_type')
	class Meta:
		model = Goods
		fields = ('url','id','types','name','price','remark')

class GoodsImageSerializer(serializers.HyperlinkedModelSerializer):
	goods=serializers.HyperlinkedRelatedField(read_only=True,view_name='image_goods')
	class Meta:
		model = GoodsImage
		fields = ('url','id','goods','image')

class CartItemSerializer(serializers.HyperlinkedModelSerializer):
	goods=serializers.HyperlinkedRelatedField(read_only=True,view_name='cart_goods')
	user=serializers.HyperlinkedRelatedField(read_only=True,view_name='cart_user')
	class Meta:
		model = CartItem
		fields = ('url','id','goods','user','count')

class OrderSerializer(serializers.HyperlinkedModelSerializer):
	user=serializers.HyperlinkedRelatedField(read_only=True,view_name='order_user')
	class Meta:
		model = Order
		fields = ('url','id','number','user','state','price','recipientName','recipientTel','recipientAddress','creat_at')

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
	order=serializers.HyperlinkedRelatedField(read_only=True,view_name='order')
	goods=serializers.HyperlinkedRelatedField(read_only=True,view_name='order_goods')
	class Meta:
		model = OrderItem
		fields = ('url','id','goods','order','goods_count','goods_name','goods_price','goods_amount')

class PostSerializer(serializers.HyperlinkedModelSerializer):
	order=serializers.HyperlinkedRelatedField(read_only=True,view_name='post_order')
	class Meta:
		model = Post
		fields = ('url','id','order','post_company','post_number')				


		