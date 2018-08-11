from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserFavSerializer
from .models import UserFav
from .permissions import IsOwnerOrReadOnly

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
    
    serializer_class = UserFavSerializer
    queryset = UserFav.objects.all()
    
    # 按照goods_id茶找
    lookup_field = 'goods_id'
    
    # 理论上不需要IsOwnerOrReadOnly 因为get_queryset已经起到了过滤user的作用
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
