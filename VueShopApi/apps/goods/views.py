from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GoodsListView(APIView):
    """
    List all goods
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # 所有数据被包装进了data中
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GoodsCategoryListView(APIView):
    """
    List all goodscatetory
    """
    def get(self, request, format=None):
        goodscategory = GoodsCategory.objects.all()[:10]
        serializer = CategorySerializer(goodscategory, many=True)
        return Response(serializer.data)
