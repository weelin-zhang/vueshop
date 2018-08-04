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
import xadmin
from django.views.static import serve
from VueShopApi.settings import MEDIA_ROOT
from goods.views import GoodsListView, GoodsCategoryListView
# 自动生成drf文档,依赖coreapi
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 商品列表页
    url(r'goods/$', GoodsListView.as_view()),

    # 商品类别列表页
    url(r'categorys/$', GoodsCategoryListView.as_view()),

    #
    url(r'^api-auth/', include('rest_framework.urls')),

    # 文档
    url(r'docs/', include_docs_urls(title="慕学生鲜"))
]


# from django.conf.urls.static import static
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)