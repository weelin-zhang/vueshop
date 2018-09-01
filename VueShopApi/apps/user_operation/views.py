from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserFavSerializer
from .serializers import UserFavDetailSerializer
from .models import UserFav
from .permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .serializers import AddressSerialzer, LeaveMessageSerializer
from .models import UserAddress, UserLeavingMessage
from goods.models import Goods

# Create your views here.


class UserFavViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    '''
    list:
        获取登录用户收藏列表
    create:
        用户收藏
    delete:
        用户取消收藏
    read:
        获取收藏信息
        
    '''
    # 权限相关
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = UserFav.objects.all()
    
    # 按照goods_id茶找
    lookup_field = 'goods_id'
    
    # 理论上不需要IsOwnerOrReadOnly 因为get_queryset已经起到了过滤user的作用
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
    
    
    # 动态serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        return UserFavSerializer

    # 点赞数+1
    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()
        
    # 点赞-1
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()
        instance.delete()

class AddressViewSet(ModelViewSet):
    '''
    list:
        获取地址表
    create:
        创建地址
    delete:
        删除地址
    retrieve:
        获取地址信息
    update:
        更新地址
    '''
    serializer_class = AddressSerialzer
    queryset = UserAddress.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
    
    
class LeaveMessageViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    '''
    list:
        获取留言IE表
    create:
        创建留言
    delete:
        删除留言
    '''
    serializer_class = LeaveMessageSerializer
    queryset = UserLeavingMessage.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    
    
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)
