# 文件名：mobile/utils/validators.py
# 参考名称：16_数据验证工具
# 说明：数据验证辅助工具


class Validators:
    """数据验证工具类"""

    @staticmethod
    def is_empty(value):
        """检查是否为空"""
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, list) and len(value) == 0:
            return True
        return False

    @staticmethod
    def validate_recipe_name(name):
        """验证菜谱名称"""
        if Validators.is_empty(name):
            return False, "菜谱名称不能为空"
        if len(name) < 2:
            return False, "菜谱名称至少 2 个字符"
        if len(name) > 50:
            return False, "菜谱名称不能超过 50 个字符"
        return True, ""

    @staticmethod
    def validate_description(description):
        """验证描述"""
        if Validators.is_empty(description):
            return True, ""  # 描述可选
        if len(description) > 500:
            return False, "描述不能超过 500 个字符"
        return True, ""

    @staticmethod
    def validate_cooking_time(cooking_time):
        """验证烹饪时间"""
        if cooking_time is None:
            return True, ""  # 可选
        try:
            time_val = int(cooking_time)
            if time_val <= 0 or time_val > 1440:  # 最多 24 小时
                return False, "烹饪时间必须在 1-1440 分钟之间"
            return True, ""
        except (ValueError, TypeError):
            return False, "烹饪时间必须是数字"

    @staticmethod
    def validate_servings(servings):
        """验证份量"""
        if servings is None:
            return True, ""  # 可选
        try:
            servings_val = int(servings)
            if servings_val <= 0 or servings_val > 100:
                return False, "份量必须在 1-100 人之间"
            return True, ""
        except (ValueError, TypeError):
            return False, "份量必须是数字"

    @staticmethod
    def validate_ingredients(ingredients):
        """验证食材列表"""
        if not ingredients:
            return True, ""  # 可选
        if not isinstance(ingredients, list):
            return False, "食材必须是列表格式"
        for ingredient in ingredients:
            if not ingredient or len(ingredient.strip()) == 0:
                return False, "食材项不能为空"
        return True, ""

    @staticmethod
    def validate_steps(steps):
        """验证步骤列表"""
        if not steps:
            return False, "至少需要一个步骤"
        if not isinstance(steps, list):
            return False, "步骤必须是列表格式"
        for step in steps:
            if not step or len(step.strip()) == 0:
                return False, "步骤内容不能为空"
        return True, ""

    @staticmethod
    def validate_category_name(name):
        """验证类别名称"""
        if Validators.is_empty(name):
            return False, "类别名称不能为空"
        if len(name) < 2:
            return False, "类别名称至少 2 个字符"
        if len(name) > 20:
            return False, "类别名称不能超过 20 个字符"
        return True, ""

    @staticmethod
    def validate_recipe_data(recipe_data, is_edit=False):
        """验证完整的菜谱数据"""
        errors = []

        # 验证名称
        valid, msg = Validators.validate_recipe_name(recipe_data.get('title'))
        if not valid:
            errors.append(msg)

        # 验证描述
        valid, msg = Validators.validate_description(recipe_data.get('description'))
        if not valid:
            errors.append(msg)

        # 验证烹饪时间
        valid, msg = Validators.validate_cooking_time(recipe_data.get('cooking_time'))
        if not valid:
            errors.append(msg)

        # 验证份量
        valid, msg = Validators.validate_servings(recipe_data.get('servings'))
        if not valid:
            errors.append(msg)

        # 验证食材
        valid, msg = Validators.validate_ingredients(recipe_data.get('ingredients'))
        if not valid:
            errors.append(msg)

        # 验证步骤
        valid, msg = Validators.validate_steps(recipe_data.get('steps'))
        if not valid:
            errors.append(msg)

        if errors:
            return False, "\n".join(errors)
        return True, ""
