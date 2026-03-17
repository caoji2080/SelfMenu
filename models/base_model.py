"""
基础模型类
"""
from datetime import datetime
from typing import Optional, Dict, Any


class BaseModel:
    """基础模型类，提供通用的序列化和反序列化方法"""

    def __init__(self, id: Optional[int] = None,
                 created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        self.id = id
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """从字典创建实例"""
        params = {k: v for k, v in data.items()
                  if k in cls.__init__.__code__.co_varnames}
        return cls(**params)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
