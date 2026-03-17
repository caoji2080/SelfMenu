"""
类别业务逻辑处理
"""
from typing import List, Dict, Optional, Tuple
from models.category_model import Category
from repositories.category_repository import CategoryRepository
from utils.validators import Validator
from app_config import DEFAULT_CATEGORIES

class CategoryService:
    """类别业务服务类"""

    def __init__(self):
        self.category_repo = CategoryRepository()
        self.validator = Validator()

    def create_category(self, category_data: Dict) -> Tuple[bool, str, Optional[int]]:
        """创建类别"""
        # 数据验证
        valid, msg = self.validator.validate_category_name(category_data.get('name', ''))
        if not valid:
            return False, msg, None

        # 检查是否重名
        existing = self.category_repo.find_by_name(category_data['name'])
        if existing:
            return False, "类别名称已存在", None

        try:
            category_id = self.category_repo.insert(category_data)
            return True, f"类别 '{category_data.get('name')}' 创建成功！", category_id
        except Exception as e:
            return False, f"创建失败：{str(e)}", None

    def update_category(self, category_id: int, category_data: Dict) -> Tuple[bool, str]:
        """更新类别"""
        if not self.category_repo.exists(category_id):
            return False, "类别不存在"

        # 如果修改了名称，检查是否重名
        if 'name' in category_data:
            existing = self.category_repo.find_by_name(category_data['name'])
            if existing and existing['id'] != category_id:
                return False, "类别名称已存在"

        try:
            self.category_repo.update(category_id, category_data)
            return True, "类别更新成功！"
        except Exception as e:
            return False, f"更新失败：{str(e)}"

    def delete_category(self, category_id: int) -> Tuple[bool, str]:
        """删除类别"""
        if not self.category_repo.exists(category_id):
            return False, "类别不存在"

        # 检查是否有菜谱使用该类别
        if self.category_repo.has_recipes(category_id):
            return False, "该类别下存在菜谱，无法删除"

        try:
            self.category_repo.delete(category_id)
            return True, "类别删除成功！"
        except Exception as e:
            return False, f"删除失败：{str(e)}"

    def get_category(self, category_id: int) -> Optional[Category]:
        """获取类别详情"""
        data = self.category_repo.find_by_id(category_id)
        return Category(**data) if data else None

    def get_all_categories(self) -> List[Category]:
        """获取所有类别"""
        categories = self.category_repo.find_all_with_count()
        return [Category(**c) for c in categories]

    def add_default_categories(self) -> Tuple[bool, str, int]:
        """添加默认类别"""
        count = 0
        for default in DEFAULT_CATEGORIES:
            existing = self.category_repo.find_by_name(default['name'])
            if not existing:
                success, _, _ = self.create_category(default)
                if success:
                    count += 1

        return True, f"已添加 {count} 个默认类别", count

    def move_up(self, category_id: int) -> bool:
        """上移类别"""
        category = self.category_repo.find_by_id(category_id)
        if not category or category['sort_order'] == 0:
            return False

        # 找到上一个类别
        prev_sql = """
            SELECT id FROM categories 
            WHERE sort_order = ? 
            LIMIT 1
        """
        prev = self.category_repo.db.fetchone(prev_sql, (category['sort_order'] - 1,))

        if prev:
            return self.category_repo.swap_sort_order(category_id, prev['id'])
        return False

    def move_down(self, category_id: int) -> bool:
        """下移类别"""
        category = self.category_repo.find_by_id(category_id)
        if not category:
            return False

        # 找到下一个类别
        next_sql = """
            SELECT id FROM categories 
            WHERE sort_order = ? 
            LIMIT 1
        """
        next_cat = self.category_repo.db.fetchone(next_sql, (category['sort_order'] + 1,))

        if next_cat:
            return self.category_repo.swap_sort_order(category_id, next_cat['id'])
        return False
