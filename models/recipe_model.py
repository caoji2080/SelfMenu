
"""
菜谱数据模型定义
"""
from typing import Optional
from models.base_model import BaseModel
from app_config import DIFFICULTY_LEVELS


class Recipe(BaseModel):
    """菜谱数据模型"""

    def __init__(self,
                 title: str = "",
                 description: str = "",
                 category_id: Optional[int] = None,
                 ingredients: str = "",
                 steps: str = "",
                 cooking_time: int = 0,
                 difficulty: str = "简单",
                 servings: int = 1,
                 image_path: Optional[str] = None,
                 status: str = "draft",
                 tags: str = "",
                 rating: float = 0.0,
                 view_count: int = 0,
                 category_name: str = "",
                 id: Optional[int] = None,
                 created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        super().__init__(id, created_at, updated_at)
        self.title = title
        self.description = description
        self.category_id = category_id
        self.ingredients = ingredients
        self.steps = steps
        self.cooking_time = cooking_time
        self.difficulty = difficulty
        self.servings = servings
        self.image_path = image_path
        self.status = status
        self.tags = tags
        self.rating = rating
        self.view_count = view_count
        self.category_name = category_name

    @property
    def difficulty_display(self) -> str:
        """难度星级显示"""
        icons = {'简单': '⭐', '中等': '⭐⭐', '困难': '⭐⭐⭐', '专家': '⭐⭐⭐⭐'}
        return icons.get(self.difficulty, '⭐')

    @property
    def time_display(self) -> str:
        """烹饪时间显示"""
        if self.cooking_time < 60:
            return f"{self.cooking_time}分钟"
        hours = self.cooking_time // 60
        minutes = self.cooking_time % 60
        return f"{hours}小时{minutes}分钟" if minutes > 0 else f"{hours}小时"

    @property
    def is_published(self) -> bool:
        """是否已发布"""
        return self.status == 'published'

    def to_dict(self) -> dict:
        """转换为字典"""
        base_dict = super().to_dict()
        base_dict.update({
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id,
            'ingredients': self.ingredients,
            'steps': self.steps,
            'cooking_time': self.cooking_time,
            'difficulty': self.difficulty,
            'servings': self.servings,
            'image_path': self.image_path,
            'status': self.status,
            'tags': self.tags,
            'rating': self.rating,
            'view_count': self.view_count,
            'category_name': self.category_name
        })
        # 插入/更新时不传递时间戳字段和虚拟字段，由数据库自动生成或查询时关联
        base_dict.pop('created_at', None)
        base_dict.pop('updated_at', None)
        base_dict.pop('category_name', None)
        return base_dict

    def __str__(self):
        return f"Recipe(id={self.id}, title='{self.title}', status='{self.status}')"
