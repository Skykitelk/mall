#!/venv/bin/env python
# -*- coding: utf-8 -*-
#copyRight by yangguozhanzhao 
# 数据模型文件，user为复写了系统的user模型

from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
	def create_user(self, openId,name, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not openId:
			raise ValueError('Users must have an openId')

		user = self.model(
			openId=openId,
			name=name,
		)
		user.set_password("1234pttk")
		print "password"
		user.save(using=self._db)
		return user

	def create_superuser(self, openId,name, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			openId,
			password=password,
			name=name,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	openId = models.CharField(
		verbose_name='openId',
		max_length=50,
		unique=True,
	)
	name=models.CharField(max_length=100)
	gender=models.IntegerField(default=1)
	avatar = models.URLField()
	create_at=models.DateTimeField(auto_now_add=True)
	update_at=models.DateTimeField(auto_now=True)
	
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	objects = MyUserManager()
	USERNAME_FIELD = 'openId'
	REQUIRED_FIELDS = ['name']
	def get_full_name(self):
		# The user is identified by their email address
		return self.name

	def get_short_name(self):
		# The user is identified by their email address
		return self.name

	def __str__(self):
	# __unicode__ on Python 2
		return self.name

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True
	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	def __unicode__(self):
		return '%s'%(self.name)


# 收货地址 多对一 用户
class Address(models.Model):
	name=models.CharField(max_length=20)
	address=models.CharField(max_length=200,blank=True)
	tel = models.CharField(max_length=12,blank=True)
	is_def=models.BooleanField(default=False)
	user=models.ForeignKey(MyUser,related_name="address")
	create_at=models.DateTimeField(auto_now_add=True)
	update_at=models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '%s,%s,%s' % (self.name,self.tel ,self.address)
		

#产品模型
class Goods(models.Model):
	types=models.ManyToManyField("Classify",related_name="goods_type")
	name=models.CharField(max_length=200,blank=True)
	mainImage=models.ImageField(upload_to='image',null=True)
	price=models.FloatField(default=0.00)
	remark=models.CharField(max_length=500,null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		# unique_together = ('album', 'order')
		ordering = ['-update_at']

	def __unicode__(self):
		return '%s'%(self.name)


# 产品类别
class Classify(models.Model):
	name=models.CharField(max_length=20)
	remark=models.CharField(max_length=200,null=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s'%(self.name)

		
# 产品图片 多对一 产品
class GoodsImage(models.Model):
	image=models.ImageField(upload_to='image', null=True)
	goods=models.ForeignKey(Goods,related_name="image")
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s'%(self.goods)

# 购物车
class CartItem(models.Model):
	goods=models.ForeignKey(Goods,related_name="cart_goods")
	count=models.IntegerField(default=1)
	user=models.ForeignKey(MyUser,related_name="cart_user")
	selected=models.BooleanField(default=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('goods', 'user')
		ordering = ['create_at']
	def __unicode__(self):
		return '%s'%(self.user)


# 订单信息 部分信息需要静态保存如收货人信息，商品信息
class Order(models.Model):
	number=models.CharField(max_length=30)
	user=models.ForeignKey(MyUser,related_name="order_user")
	state = models.PositiveSmallIntegerField(default=0)
	price = models.FloatField(default=0.00)
	recipientName=models.CharField(max_length=20)
	recipientTel=models.CharField(max_length=12,blank=True)
	recipientAddress=models.CharField(max_length=200,blank=True)	

	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s'%(self.number)

class OrderItem(models.Model):
	order=models.ForeignKey(Order,related_name="order")
	goods=models.ForeignKey(Goods,related_name="order_goods")
	goods_count = models.IntegerField(verbose_name=u"商品数量", blank=True, null=True)
	goods_name = models.CharField(verbose_name="商品名称", blank=True, max_length=100)
	goods_price = models.FloatField(verbose_name=u"商品单价", default=0.0)
	goods_amount = models.FloatField(verbose_name=u"商品总价", default=0.0)
	def __unicode__(self):
		return '%s'%(self.goods_name)

#发货信息
class Post(models.Model):
	order=models.OneToOneField(Order,related_name="post_order")
	post_company=models.CharField(max_length=10)
	post_number=models.CharField(max_length=20)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s'%(self.post_number)
				




