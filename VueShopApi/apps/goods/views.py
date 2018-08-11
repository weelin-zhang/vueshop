from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
# 过滤用
from django_filters import rest_framework as filters
from .filters import GoodsFilter
# search 用
from rest_framework.filters import SearchFilter
# 排序用
from rest_framework.filters import OrderingFilter

#from rest_framework.authentication import  SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# 深度定制分页, 可以达到前端动态设置效果
class GoodsPagination(PageNumberPagination):
    page_size = 12
    # page_size 提供动态设置分页的功能
    page_size_query_param = 'page_size'
    # 默认page(?page=2)
    page_query_param = 'page'
    max_page_size = 100
    
### 使用viewSet

class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # authentication_classes = (SessionAuthentication,)
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    
    '''
    分页 搜索 过滤 排序
    http://localhost:8000/api/v1/goods/?ordering=-shop_price&search=%E7%89%9B%E8%82%89&min_price=200
    '''
    # 当没有重写get_queryset时,一定要定义queryset属性
    queryset = Goods.objects
    serializer_class = GoodsSerializer
    
    # 分页
    pagination_class = GoodsPagination
    
    # 这种过滤方式太过单一，无法指定范围
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ['name','shop_price']
    
    # 自定义filterSet
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = GoodsFilter
    
    # search
    # search框的输入会在所有的search_fields字段中查找,理解为并集
    # field可以使该model字段,也可以是related, manytomany字段
    # search_fields = ('=username', '$email', '^goods_desc') 分别表示精确匹配,正则, 以..开头
    search_fields = ['name', 'goods_desc', 'goods_brief', 'category__name']
    
    # 排序, 不指定search_fields的话,会允许所有字段的排序
    ordering_fields = ['shop_price','sold_num']
    # query_params不指定ordering时的默认排序方式
    ordering=('-add_time',)
    
    # 排序
    
    # 使用get_queryset和request.query_params实现动态过滤功能
    # def get_queryset(self):
    #     # 最低价格
    #     price_min = self.request.query_params.get('price_min', 0)
    #
    #     return Goods.objects.filter(shop_price__gt=int(price_min))
    

class CategroyListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    read:
        商品分类详情
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
    
    
    # 根据api规范重写
    # def get_object(self):
    #     if not self.queryset or not self.queryset.filter(**self.kwargs):
    #         return
    #     return super().get_object()
    #
    # # 定制一下返回结果
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if not instance:
    #         return Response({"msg": 'no exists', "code": "1"})
    #     serializer = self.get_serializer(instance)
    #     data = {"msg": "success", "code": "0", "data": serializer.data}
    #     return Response(data)

# 需要轮播的商品
class BannerListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    list:
        需要轮播的商品
    '''
    serializer_class = BannerSerializer
    queryset = Banner.objects
    
