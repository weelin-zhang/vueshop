import re
import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.validators import UniqueValidator
User = get_user_model()
from .models import ShoppingCart
from goods.models import Goods


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        "min_value": "商品数量不能小于1",
        "required": "请选择数量"
    }, label='数量', help_text="商品数量")
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True, label="商品", help_text="商品")
    
    # 必须重写, Serializer没提供
    def create(self, valicated_data):
        '''
        :param valicated_data: 处理后的数据
        :return:
        '''
        user = self.context['request'].user
        nums = valicated_data['nums']
        goods = valicated_data['goods']
        
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(user=user, goods=goods, nums=nums)
        
        return  existed


    # 必须重写, Serializer没提供
    def update(self, instance, validated_data):
        nums = validated_data['nums']
        instance.nums = nums
        instance.save()
        return instance
        
        
    



