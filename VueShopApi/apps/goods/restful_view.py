'''
记录各种类的使用方法
'''
from .serializers import GoodsSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .models import Goods, GoodsCategory


# 深度定制分页, 可以达到前端动态设置效果
class GoodsPagination(PageNumberPagination):
    page_size = 20
    # page_size 提供动态设置分页的功能
    page_size_query_param = 'page_size'
    # 默认page(?page=2)
    page_query_param = 'p'
    max_page_size = 100


### 使用viewSet

class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


# # 深度定制分页, 可以达到前端动态设置效果
# class GoodsPagination(PageNumberPagination):
#     page_size = 10
#     # page_size 提供动态设置分页的功能
#     page_size_query_param = 'page_size'
#     # 默认page(?page=2)
#     page_query_param = 'p'
#     max_page_size = 100

# 进一步封装成最简形式
class GoodsListView(generics.ListAPIView):
    '''
    商品列表页
    '''
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


    def get_queryset(self):
        return Goods.objects.all()

# 在APIView基础上封装
# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     '''
#     商品列表页
#     '''
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# APIView实现
# class GoodsListView(APIView):
#     """
#     List all goods
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)



class GoodsCategoryListView(APIView):
    """
    List all goodscatetory
    """
    
    def get(self, request, format=None):
        goodscategory = GoodsCategory.objects.all()
        serializer = CategorySerializer(goodscategory, many=True)
        return Response(serializer.data)