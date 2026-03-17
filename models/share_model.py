"""
分享记录数据模型
"""
from typing import Optional
from models.base_model import BaseModel


class ShareRecord(BaseModel):
    """分享记录模型"""

    def __init__(self,
                 recipe_id: int = 0,
                 share_method: str = "",
                 share_target: str = "",
                 share_content: str = "",
                 recipe_title: str = "",
                 id: Optional[int] = None,
                 created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        super().__init__(id, created_at, updated_at)
        self.recipe_id = recipe_id
        self.share_method = share_method
        self.share_target = share_target
        self.share_content = share_content
        self.recipe_title = recipe_title
        self.shared_at = created_at

    def to_dict(self) -> dict:
        """转换为字典"""
        base_dict = super().to_dict()
        base_dict.update({
            'recipe_id': self.recipe_id,
            'share_method': self.share_method,
            'share_target': self.share_target,
            'share_content': self.share_content,
            'recipe_title': self.recipe_title,
            'shared_at': self.shared_at
        })
        return base_dict
