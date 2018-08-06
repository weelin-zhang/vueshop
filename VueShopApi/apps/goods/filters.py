from django_filters import rest_framework as filters
from .models import Goods
from django.db.models import Q

class GoodsFilter(filters.FilterSet):
    '''
    前端可以使用下面样式得到价格区间在[50,70]元的商品
    http://localhost:8000/api/v1/goods/?min_price=50&max_price=70
    
    增加水果的模糊匹配
    http://localhost:8000/api/v1/goods/?min_price=50&max_price=70&goodsname='水果'
    '''
    # 此时min_price字段表示大于等于query_params传入的值
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    # 此时max_price字段表示小于等于query_params传入的值
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')

    top_category = filters.NumberFilter(method='top_category_filter', field_name="top_category")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category__id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    #goodsname = filters.CharFilter(field_name='name', lookup_expr='icontains')
    # 精确匹配
    # goodsname = filters.CharFilter(field_name='name', lookup_expr='iexact')
    class Meta:
        model = Goods
        # 列表中字段默认是精确匹配
        fields = ['pricemin', 'pricemax', 'top_category', 'is_new','is_hot']
