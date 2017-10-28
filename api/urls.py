#!/usr/bin/env python
# -*- coding: utf-8 -*-
#copyRight by yangguozhanzhao 
#应用api的urls配置

from django.conf.urls import url,include
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'address', views.AddressViewSet)
router.register(r'classify', views.ClassifyViewSet)
router.register(r'goods', views.GoodsViewSet)
router.register(r'goodsimage', views.GoodsImageViewSet)
router.register(r'cartitem', views.CartItemViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'orderitem', views.OrderItemViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'swiper', views.SwiperViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='Workers API')),
    url(r'^token/', obtain_jwt_token),
    url(r'^login/',views.login),
    url(r'^unifiedorder/',views.unifiedorder),
    url(r'^myorder/',views.myOrder),
    #url(r'^workers/?(?P<pk>\d+)/$',views.workers),
    #url(r'^invitations/?(?P<pk>\d+)/$',views.invitation),
    #url(r'^avatar/',views.updateAvatar),
    #url(r'^getday/',views.getDayData),
    #url(r'^getstaff/',views.getStaff),
]
