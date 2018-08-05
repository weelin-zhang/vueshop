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
from goods.views import GoodsListViewSet, CategroyListViewSet
from rest_framework.routers import DefaultRouter
# 自动生成drf文档,依赖coreapi
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register('goods', GoodsListViewSet)
router.register('categorys', CategroyListViewSet)

# 有了router不需要了
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
    
    # viewset 大法
    url(r'^api/v1/', include(router.urls), name='goods-list'),

    # 商品列表页
    # url(r'goods/$', goods_list, name='goods-list'),

    # 商品类别列表页
    # url(r'^categorys/$', GoodsCategoryListView.as_view()),
    
    # url(r'^goods/$', GoodsListView.as_view()),

    #
    url(r'^api-auth/', include('rest_framework.urls')),

    # 文档
    url(r'^api/docs/', include_docs_urls(title="慕学生鲜"))
]


# from django.conf.urls.static import static
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)