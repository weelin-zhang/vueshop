import re
import datetime
from rest_framework import serializers
from .models import VerifyCode
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.validators import UniqueValidator
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
            
            

class UserRegsSerializer(serializers.ModelSerializer):
    # code这个字段用户字段没有，但是要用它来决定是否可以注册,所以要定义出来
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, help_text='验证码',
                                 error_messages={
        "require": "请输入验证码",
        "min_length": "四位数字",
        "max_length": "四位数字",
        "blank": "不能为空"
    }, label="验证码")
    
    password = serializers.CharField(style={"input_type": "password"}, label="密码")
    # 验证是否唯一
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在"),],
                                     label="用户名")
    
    class Meta:
        model = User
        # 后面code会删掉,因为model中并么有这个code字段
        fields = ('username', 'password', 'code', 'mobile')
        
    
    def validate_code(self, code):
        # 是否过期
        five_mintues_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
        # initial 是传过来的值
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_codes:
            last_record = verify_codes[0]
            if five_mintues_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期了")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")
        
        return code
        
    # 解决code多与问题
    def validate(self, attrs):
       
        # 删除多余的code
        # 必须删掉, 因为model里没有它的位置
        del attrs['code']
        # 前端没传值, 可以在这里添加, 因为模型中mobile为null=True，所以前端可以不传
        attrs['mobile'] = attrs['username']
        
        return attrs
    
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
