"""
菜谱业务逻辑处理
"""
from typing import List, Dict, Optional, Tuple
from models.recipe_model import Recipe
from repositories.recipe_repository import RecipeRepository
from repositories.category_repository import CategoryRepository
from utils.validators import Validator

class RecipeService:
    """菜谱业务服务类"""

    def __init__(self):
        self.recipe_repo = RecipeRepository()
        self.category_repo = CategoryRepository()
        self.validator = Validator()

    def create_recipe(self, recipe_data: Dict) -> Tuple[bool, str, Optional[int]]:
        """创建菜谱"""
        # 数据验证
        valid, msg = self.validator.validate_recipe_title(recipe_data.get('title', ''))
        if not valid:
            return False, msg, None

        # 将列表转换为字符串（如果传入的是列表）
        ingredients = recipe_data.get('ingredients', '')
        if isinstance(ingredients, list):
            ingredients = "\n".join(ingredients)
            recipe_data['ingredients'] = ingredients

        steps = recipe_data.get('steps', '')
        if isinstance(steps, list):
            steps = "\n".join(steps)
            recipe_data['steps'] = steps

        valid, msg = self.validator.validate_ingredients(ingredients)
        if not valid:
            return False, msg, None

        valid, msg = self.validator.validate_steps(steps)
        if not valid:
            return False, msg, None

        valid, msg = self.validator.validate_cooking_time(recipe_data.get('cooking_time', 0))
        if not valid:
            return False, msg, None

        try:
            # 插入数据库
            recipe_id = self.recipe_repo.insert(recipe_data)
            return True, f"菜谱 '{recipe_data.get('title')}' 创建成功！", recipe_id
        except Exception as e:
            return False, f"创建失败：{str(e)}", None

    def update_recipe(self, recipe_id: int, recipe_data: Dict) -> Tuple[bool, str]:
        """更新菜谱"""
        if not self.recipe_repo.exists(recipe_id):
            return False, "菜谱不存在"

        # 数据验证
        if 'title' in recipe_data:
            valid, msg = self.validator.validate_recipe_title(recipe_data['title'])
            if not valid:
                return False, msg

        # 将列表转换为字符串（如果传入的是列表）
        if 'ingredients' in recipe_data:
            ingredients = recipe_data['ingredients']
            if isinstance(ingredients, list):
                ingredients = "\n".join(ingredients)
                recipe_data['ingredients'] = ingredients

        if 'steps' in recipe_data:
            steps = recipe_data['steps']
            if isinstance(steps, list):
                steps = "\n".join(steps)
                recipe_data['steps'] = steps

        try:
            self.recipe_repo.update(recipe_id, recipe_data)
            return True, "菜谱更新成功！"
        except Exception as e:
            return False, f"更新失败：{str(e)}"

    def delete_recipe(self, recipe_id: int) -> Tuple[bool, str]:
        """删除菜谱"""
        if not self.recipe_repo.exists(recipe_id):
            return False, "菜谱不存在"

        try:
            self.recipe_repo.delete(recipe_id)
            return True, "菜谱删除成功！"
        except Exception as e:
            return False, f"删除失败：{str(e)}"

    def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        """获取菜谱详情"""
        data = self.recipe_repo.find_with_category(recipe_id)
        return Recipe(**data) if data else None

    def get_all_recipes(self, page: int = 1, page_size: int = 10) -> List[Recipe]:
        """获取所有菜谱（分页）"""
        offset = (page - 1) * page_size
        recipes = self.recipe_repo.find_all_with_category(limit=page_size, offset=offset)
        return [Recipe(**r) for r in recipes]

    def get_recipes_by_category(self, category_id: int) -> List[Recipe]:
        """根据类别获取菜谱"""
        recipes = self.recipe_repo.find_by_category(category_id)
        return [Recipe(**r) for r in recipes]

    def search_recipes(self, keyword: str) -> List[Recipe]:
        """搜索菜谱"""
        recipes = self.recipe_repo.search_by_keyword(keyword)
        return [Recipe(**r) for r in recipes]

    def search_advanced(self, filters: Dict) -> List[Recipe]:
        """高级搜索"""
        recipes = self.recipe_repo.search_advanced(filters)
        return [Recipe(**r) for r in recipes]

    def get_published_recipes(self) -> List[Recipe]:
        """获取已发布的菜谱"""
        recipes = self.recipe_repo.find_by_status('published')
        return [Recipe(**r) for r in recipes]

    def get_draft_recipes(self) -> List[Recipe]:
        """获取草稿菜谱"""
        recipes = self.recipe_repo.find_by_status('draft')
        return [Recipe(**r) for r in recipes]

    def get_recent_recipes(self, limit: int = 10) -> List[Recipe]:
        """获取最近的菜谱"""
        recipes = self.recipe_repo.get_recent_recipes(limit)
        return [Recipe(**r) for r in recipes]

    def get_popular_recipes(self, limit: int = 10) -> List[Recipe]:
        """获取热门菜谱"""
        recipes = self.recipe_repo.get_popular_recipes(limit)
        return [Recipe(**r) for r in recipes]

    def increment_view_count(self, recipe_id: int) -> bool:
        """增加浏览次数"""
        return self.recipe_repo.increment_view_count(recipe_id)

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return self.recipe_repo.get_statistics()
