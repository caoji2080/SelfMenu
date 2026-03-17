# 文件名：mobile/services/category_service_mobile.py
# 参考名称：14_类别服务（移动端）
# 说明：为移动端提供类别相关的业务逻辑

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 使用绝对导入
from services.category_service import CategoryService


class CategoryServiceMobile:
    """移动端类别服务 - 封装原有服务以适应移动端"""

    def __init__(self):
        self.service = CategoryService()

    # ... existing code ...
