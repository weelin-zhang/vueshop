from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrdersSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods

class ShopingCartViewSet(viewsets.ModelViewSet):
    '''
    list:
        用户购物车列表
    create:
        添加商品
    delete:
        删除商品
    read:
        购物车详情
    update:
        修改购物车
    '''

    serializer_class = ShopCartSerializer
    queryset = ShoppingCart.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'
    
    
    # 自定义serializer
    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        return ShopCartSerializer
    
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrdersViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    '''
    list:
        订单列表
    read:
        订单详情
    create:
        创建订单
    delete:
        删除订单
    '''
    
    
    serializer_class = OrdersSerializer
    queryset = OrderInfo.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
   
    
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        order = serializer.save()
        shoppingcarts = ShoppingCart.objects.filter(user=self.request.user)
        for sc in shoppingcarts:
            OrderGoods.objects.create(goods=sc.goods, goods_num=sc.nums, order=order)
            sc.delete()
        order.save()
        
