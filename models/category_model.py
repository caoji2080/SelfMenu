
"""
类别数据模型定义
"""
from typing import Optional
from models.base_model import BaseModel
from app_config import CATEGORY_ICONS


class Category(BaseModel):
    """菜谱类别数据模型"""

    def __init__(self,
                 name: str = "",
                 description: str = "",
                 icon: str = "🍽️",
                 sort_order: int = 0,
                 recipe_count: int = 0,
                 id: Optional[int] = None,
                 created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        super().__init__(id, created_at, updated_at)
        self.name = name
        self.description = description
        self.icon = icon or CATEGORY_ICONS.get(name, "🍽️")
        self.sort_order = sort_order
        self.recipe_count = recipe_count

    @property
    def display_name(self) -> str:
        """显示名称（带图标）"""
        return f"{self.icon} {self.name}"

    def to_dict(self) -> dict:
        """转换为字典"""
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'recipe_count': self.recipe_count
        })
        return base_dict

    def __str__(self):
        return f"Category(id={self.id}, name='{self.name}', icon='{self.icon}')"
