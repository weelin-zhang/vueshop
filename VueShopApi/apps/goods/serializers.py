from rest_framework import serializers
from .models import Goods, GoodsCategory
from .models import Banner
from .models import GoodsImage
from .models import HotSearchWords
from .models import GoodsCategoryBrand
from .models import IndexAd
from django.db.models import Q

# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Goods` instance, given the validated data.
#         """
#         print(validated_data)
#         return Goods.objects.create(**validated_data)

class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'
        
        
class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'
    

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
    # 拿到子类
    # sub_cat 必须和外键的related_name一致
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        # fields = ['name', 'parent_category', 'id', 'is_tab', 'category_type', 'desc', 'code', 'add_time', 'goods_set']
        fields = "__all__"

        #自定义模式
        # fields = ['name', 'parent_category', 'id', 'is_tab', 'category_type', 'desc', 'code', 'add_time', 'goods_set']


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = '__all__'



# 商品序列化
class GoodsSerializer(serializers.ModelSerializer):
    # category时外键
    # 1. category纸打印出model.__str__()的结果
    # category = serializers.CharField()

    # 打印出category序列化后的dict
    category = CategorySerializer()
    # 轮播图片
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = "__all__"


# banner
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


# hot search

class HotSearchWordsSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = HotSearchWords
        fields = '__all__'
        

class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'
    



class AdGoodsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IndexAd
    
    
# indexCategory
class IndexCategorySerializer(serializers.ModelSerializer):
    brands = GoodsCategoryBrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()
    
    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data
    
    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)

        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json
    

    class Meta:
        model = GoodsCategory
        fields = '__all__'
    