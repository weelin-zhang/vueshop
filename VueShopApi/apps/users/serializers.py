import re
import datetime
from rest_framework import serializers
from .models import VerifyCode
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

# 不用 serializers.ModelSerializer,因为用户只输入一个电话号码
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    
    def validate_mobile(self, mobile):
        '''
        验证输入的手机号码
        '''
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError('用户已经存在')
        
        # 验证号码是否合法
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号不合法')
        
        # 一分钟发一次
        one_minute_ago = datetime.datetime.now()-datetime.timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError('距离上次发送未满60s')
            
            
        
        
        
        
    
