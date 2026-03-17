"""
数据验证工具类
"""
from typing import Tuple


class Validator:
    """数据验证工具类，提供各类数据验证方法"""

    @staticmethod
    def validate_recipe_title(title: str) -> Tuple[bool, str]:
        """验证菜谱标题"""
        if not title or len(title.strip()) == 0:
            return False, "菜谱标题不能为空"
        if len(title) > 100:
            return False, "菜谱标题不能超过 100 个字符"
        return True, ""

    @staticmethod
    def validate_description(description: str) -> Tuple[bool, str]:
        """验证描述信息"""
        if len(description) > 1000:
            return False, "描述不能超过 1000 个字符"
        return True, ""

    @staticmethod
    def validate_ingredients(ingredients) -> Tuple[bool, str]:
        """验证食材列表"""
        # 如果是列表，转换为字符串
        if isinstance(ingredients, list):
            ingredients = "\n".join(ingredients)

        if not ingredients or len(ingredients.strip()) == 0:
            return False, "食材不能为空"
        if len(ingredients) > 2000:
            return False, "食材描述不能超过 2000 个字符"
        return True, ""

    @staticmethod
    def validate_steps(steps) -> Tuple[bool, str]:
        """验证烹饪步骤"""
        # 如果是列表，转换为字符串
        if isinstance(steps, list):
            steps = "\n".join(steps)

        if not steps or len(steps.strip()) == 0:
            return False, "烹饪步骤不能为空"
        if len(steps) > 5000:
            return False, "步骤描述不能超过 5000 个字符"
        return True, ""

    @staticmethod
    def validate_cooking_time(minutes: int) -> Tuple[bool, str]:
        """验证烹饪时间"""
        if minutes < 0:
            return False, "烹饪时间不能为负数"
        if minutes > 1440:  # 24 小时
            return False, "烹饪时间不能超过 24 小时"
        return True, ""

    @staticmethod
    def validate_difficulty(difficulty: str) -> Tuple[bool, str]:
        """验证难度等级"""
        valid_difficulties = ['简单', '中等', '困难', '专家']
        if difficulty not in valid_difficulties:
            return False, f"难度必须是以下之一：{', '.join(valid_difficulties)}"
        return True, ""

    @staticmethod
    def validate_servings(count: int) -> Tuple[bool, str]:
        """验证份量人数"""
        if count <= 0:
            return False, "份数必须大于 0"
        if count > 100:
            return False, "份数不能超过 100 人"
        return True, ""

    @staticmethod
    def validate_category_name(name: str) -> Tuple[bool, str]:
        """验证类别名称"""
        if not name or len(name.strip()) == 0:
            return False, "类别名称不能为空"
        if len(name) > 50:
            return False, "类别名称不能超过 50 个字符"
        return True, ""

    @staticmethod
    def validate_tags(tags: str) -> Tuple[bool, str]:
        """验证标签"""
        if len(tags) > 200:
            return False, "标签总长度不能超过 200 个字符"
        return True, ""

    @staticmethod
    def validate_rating(rating: float) -> Tuple[bool, str]:
        """验证评分"""
        if rating < 0 or rating > 5:
            return False, "评分必须在 0-5 之间"
        return True, ""
