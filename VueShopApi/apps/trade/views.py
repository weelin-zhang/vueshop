from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import ShopCartSerializer
from .models import ShoppingCart

class ShopingCartViewSet(viewsets.ModelViewSet):
    '''
    list:
        用户购物车列表
    create:
        添加商品
    '''

    serializer_class = ShopCartSerializer
    queryset = ShoppingCart.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'
    
    
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)