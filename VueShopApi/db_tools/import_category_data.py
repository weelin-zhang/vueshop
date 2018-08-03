import os, sys
from django.core.wsgi import get_wsgi_application


PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) # 定位到你的django根目录
SETTINGS_MODULE = "VueShopApi.settings"

sys.path.append(PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)  # 你的django的settings文件
application =  get_wsgi_application()


if __name__ == "__main__":
    from goods.models import GoodsCategory
    from db_tools.data.category_data import row_data
    
    # 导入level1
    for level1 in row_data[1:]:
        level1_instance = GoodsCategory()
        level1_instance.name = level1['name']
        level1_instance.code = level1['code']
        level1_instance.category_type = 1
        level1_instance.save()
        
        
        for level2 in level1['sub_categorys']:
            level2_instance = GoodsCategory()
            level2_instance.name = level2['name']
            level2_instance.code = level2['code']
            level2_instance.category_type = 2
            level2_instance.parent_category = level1_instance
            level2_instance.save()

            for level3 in level2['sub_categorys']:
                level3_instance = GoodsCategory()
                level3_instance.name = level3['name']
                level3_instance.code = level3['code']
                level3_instance.category_type = 3
                level3_instance.parent_category = level2_instance
                level3_instance.save()
    

