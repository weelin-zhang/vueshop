import os, sys
from django.core.wsgi import get_wsgi_application

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))  # 定位到你的django根目录
# PROJECT_PATH ='/opt/zhonghua/vueshop/VueShopApi'
SETTINGS_MODULE = "VueShopApi.settings"

sys.path.append(PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)  # 你的django的settings文件
application = get_wsgi_application()


'''
{
        'images': [
            'goods/images/1_P_1449024889889.jpg',
            'goods/images/1_P_1449024889264.jpg',
            'goods/images/1_P_1449024889726.jpg',
            'goods/images/1_P_1449024889018.jpg',
            'goods/images/1_P_1449024889287.jpg'
        ],
        'categorys': [
            '首页',
            '生鲜食品',
            '根茎类'
        ],
        'market_price': '￥232元',
        'name': '新鲜水果甜蜜香脆单果约800克',
        'desc': '食用百香果可以增加胃部饱腹感，减少余热量的摄入，还可以吸附胆固醇和胆汁之类有机分子，抑制人体对脂肪的吸收。因此，长期食用有利于改善人体营养吸收结构，降低体内脂肪，塑造健康优美体态。',
        'sale_price': '￥156元',
        'goods_desc':'<p><img src="/media/goods/images/2_20170719161405_249.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161414_628.jpg" title="" alt="2.jpg"/></p><p><img src="/media/goods/images/2_20170719161435_381.jpg" title="" alt="2.jpg"/></p>'
    },
'''
'''
category = models.ForeignKey(GoodsCategory, verbose_name='商品类目')
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一货号')
    name = models.CharField(max_length=300, verbose_name='商品名')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='商品销售量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    goods_num = models.IntegerField(default=0, verbose_name='库存数')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='本店价格')
    goods_brief = models.TextField(verbose_name='商品简短描述')
    goods_desc = UEditorField(verbose_name='内容', imagePath='goods/images/', width='100%', height=300)
    ship_free = models.BooleanField(default=False)
    # 商品封面图
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    # 商品是否新品
    is_new = models.BooleanField(default=False, verbose_name='是否热销')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

'''

if __name__ == "__main__":
    from goods.models import Goods, GoodsCategory, GoodsImage
    from db_tools.data.product_data import row_data
    
    for g in row_data:
        g_instance = Goods()
        g_instance.name = g['name']
        g_instance.market_price = float(int(g["sale_price"].replace("￥", "").replace("元", "")))
        g_instance.shop_price = float(int(g["sale_price"].replace("￥", "").replace("元", "")))
        g_instance.goods_brief = g['desc'] if g['desc'] is not None else ''
        g_instance.goods_desc = g['goods_desc'] if g['goods_desc'] is not None else ''
        g_instance.goods_front_image = g['images'][0] if g['images'] else ''
        
        # 类别
        category = GoodsCategory.objects.filter(name=g['categorys'][-1])
        if category:
            g_instance.category = category[0]
        g_instance.save()
        # goodsimage
        for img in g['images']:
            good_img_instane = GoodsImage()
            good_img_instane.goods = g_instance
            good_img_instane.image = img
            good_img_instane.save()
