from rest_framework import serializers
from .models import Goods, GoodsCategory


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()


    # def create(self, validated_data):
    #     """
    #     Create and return a new `Goods` instance, given the validated data.
    #     """
    #     print(validated_data)
    #     return Goods.objects.create(**validated_data)


# 商品类别序列化
class CategorySerializer(serializers.ModelSerializer):
    '''
    1. 商品类别时商品的外键,默认情况向不会序列化 goods_set or goods

    2. 想要展示类别其下面的goods需要在fields中显式的定义
    3. 默认情况下时goods.id的列表
        eg:
            {
                "name": "海鲜水产",
                ...,
                "add_time": "2018-08-04T10:05:05.432450",
                "goods_set": [
                    2,
                    5,
                    8,
                    12
                ]
            }

    4. goods_set显示成json形式,那么必须自定义 goods_set字段
        eg:
            goods_set = GoodsSerializer(many=True)
    '''
    class Meta:
        model = GoodsCategory
        # 默认补包含一对多的多的那个model
        fields = "__all__"

        #自定义模式
        # fields = ['name', 'parent_category', 'id', 'is_tab', 'category_type', 'desc', 'code', 'add_time', 'goods_set']


# 商品序列化
class GoodsSerializer(serializers.ModelSerializer):
    # category时外键
    # 1. category纸打印出model.__str__()的结果
    # category = serializers.CharField()

    # 打印出category序列化后的dict
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = "__all__"



