from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from goods.models import Goods
from user_operation.models import UserAddress
from user_operation.models import UserLeavingMessage


class GoodsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ("shop_price", "name", "id")
    

class UserFavDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    goods =  GoodsDetailSerializer()
    class Meta:
        model = UserFav
        fields = ("user", "goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        fields = ('goods', 'user', 'id')

        # 自定义联合唯一
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        
        
class AddressSerialzer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "address", "signer_name", "signer_mobile", "id")

    
    # def validate_signer_mobile(self, signer_mobile):
    #     if len(signer_mobile) != 11:
    #         raise serializers.ValidationError("格式错误")
    #     return signer_mobile
    

class LeaveMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 不用提交，有默认值
    add_time = serializers.DateTimeField(read_only=True,format=format("%Y-%m-%d %H:%M"))
    class Meta:
        model = UserLeavingMessage
        fields = "__all__"
