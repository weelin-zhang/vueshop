from random import choice
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import VerifyCode
from rest_framework import status
from rest_framework.response import Response
from .serializers import SmsSerializer
from django.conf import settings
from rest_framework.authentication import  SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
# 注册创建用户的同时,返回token
from rest_framework_jwt.utils import  jwt_payload_handler
from rest_framework_jwt.utils import  jwt_encode_handler

# 发短信代码
from utils.yunpian import YunPian


User = get_user_model()
from .serializers import UserRegsSerializer
from .serializers import UserDetailSerializer

# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
        
        

class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    '''
    发送短信验证(后台会做记录)
    '''
    serializer_class = SmsSerializer
    queryset = VerifyCode.objects
    
    def generate(self):
        '''
        生成四位验证码
        :return:
        '''
        seeds = '1234567890'
        num_l = []
        for i in range(4):
           num_l.append(choice(seeds))
        return ''.join(num_l)
    
    # 重写create方法,因为涉及到发送短信息=问题
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 此处可自定义返回格式
        # if not serializer.is_valid(raise_exception=False):
            # print(serializer.errors['mobile'][0])
            # from rest_framework.response import Response
            # return Response({"message": serializer.errors['mobile'][0]})
        
        
        # 获取电话号码
        mobile = serializer.validated_data('mobile')
        yun_pian = YunPian(settings.APIKEY)
        # 发送
        sms_code = self.generate()
        sms_status = yun_pian.send_sms(sms_code, mobile=mobile)
        if sms_status['code'] != 0:
            return  Response({"mobile": sms_status['msg']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 保存验证码, 因为serializers.Serializer不会自动保存
            verify_code = VerifyCode(mobile=mobile, code=sms_code)
            verify_code.save()
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)
        


class UserRegViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    
    serializer_class = UserRegsSerializer
    queryset = User.objects
    
    # 这里会把认证信息和user关联起来,没这个认证，request.user是AnonymousUser
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    
    
    # 动态设置认证permission
    def get_permissions(self):
        if self.action == "create":
            return []
        elif self.action == "retrieve":
            return [IsAuthenticated(), ]
        return [IsAuthenticated(), ]
    
    # 动态设置serializer
    def get_serializer_class(self):
        if self.action == "create":
            return UserRegsSerializer
        else:
            return UserDetailSerializer
        

    # 获取用户信息时 重写get_object方法
    def get_object(self):
        return self.request.user

    # 默认返回不包含token,为了注册成功返回token,需要重写create,局部修正
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        u = self.perform_create(serializer)

        # 在此处加入token内容, 定制返回结果
        ret = serializer.data
        payload = jwt_payload_handler(u)
        token = jwt_encode_handler(payload)

        ret['token'] = token

        ret['name'] = u.name if u.name else u.username
        headers = self.get_success_headers(serializer.data)
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return  serializer.save()

