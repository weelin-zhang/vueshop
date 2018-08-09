from random import choice
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import VerifyCode
from rest_framework import status
from rest_framework.response import Response
from .serializers import SmsSerializer
from django.conf import settings

# 发短信代码
from utils.yunpian import YunPian


User = get_user_model()
from .serializers import UserRegsSerializer

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
        


class UserRegViewSet(CreateModelMixin, GenericViewSet):
    
    serializer_class = UserRegsSerializer
    queryset = User.objects
