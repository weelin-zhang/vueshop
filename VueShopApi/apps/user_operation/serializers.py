from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator



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