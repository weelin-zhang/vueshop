"""VueShopApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve
from VueShopApi.settings import MEDIA_ROOT
from goods.restful_view import GoodsListView, GoodsCategoryListView
from goods.views import GoodsListViewSet, CategroyListViewSet, BannerListViewSet, HotSearchWordsViewSet
from goods.views import IndexCategoryViewSet
from rest_framework.routers import DefaultRouter
# 自动生成drf文档,依赖coreapi
from rest_framework.documentation import include_docs_urls

# drf Token
from rest_framework.authtoken import views

# jwt Token
from rest_framework_jwt.views import obtain_jwt_token

#验证码,注册
from users.views import SmsCodeViewSet, UserRegViewSet


# 收藏
from user_operation.views import UserFavViewSet

# 地址
from user_operation.views import AddressViewSet

# 留言
from user_operation.views import LeaveMessageViewSet

# 交易
from trade.views import ShopingCartViewSet, OrdersViewSet


router = DefaultRouter()
router.register('goods', GoodsListViewSet, base_name='goods')
router.register('categorys', CategroyListViewSet, base_name='categorys')
router.register('banners', BannerListViewSet, base_name='banners')
router.register('codes', SmsCodeViewSet, base_name='codes')
router.register('users', UserRegViewSet, base_name='users')
router.register('userfavs', UserFavViewSet, base_name='userfavs')
router.register("address", AddressViewSet, base_name="address")
router.register("messages", LeaveMessageViewSet, base_name="messages")
router.register("shopcarts", ShopingCartViewSet, base_name="shopcarts")
router.register("orders", OrdersViewSet, base_name="orders")
router.register("hotsearchs", HotSearchWordsViewSet, base_name="hotsearchs")
router.register("indexgoods", IndexCategoryViewSet, base_name="indexgoods")

# 有了router不需要了
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
    
    # viewset 大法
    # url(r'^api/v1/', include(router.urls)),
    url(r'^', include(router.urls)),

    # 商品列表页
    # url(r'goods/$', goods_list, name='goods-list'),

    # 商品类别列表页
    # url(r'^categorys/$', GoodsCategoryListView.as_view()),
    
    # url(r'^goods/$', GoodsListView.as_view()),

    # 开启api认证功能
    url(r'^api-auth/', include('rest_framework.urls')),

    # drf自带的Token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt认证接口
    url(r'^login/', obtain_jwt_token),
    # url(r'^jwt_auth/', obtain_jwt_token),

    # 文档
    url(r'^api/docs/', include_docs_urls(title="慕学生鲜"))
]


# from django.conf.urls.static import static
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
