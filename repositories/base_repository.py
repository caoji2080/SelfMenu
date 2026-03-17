
"""
基础数据访问类
"""
from typing import List, Dict, Any, Optional
from utils.database import db


class BaseRepository:
    """基础 Repository 类，提供通用的 CRUD 操作"""

    table_name: str = ""

    def __init__(self):
        self.db = db

    def find_by_id(self, id: int) -> Optional[Dict]:
        """根据 ID 查找单条记录"""
        return self.db.fetchone(f"SELECT * FROM {self.table_name} WHERE id = ?", (id,))

    def find_all(self, order_by: str = "id") -> List[Dict]:
        """查询所有记录"""
        return self.db.fetchall(f"SELECT * FROM {self.table_name} ORDER BY {order_by}")

    def find_by_field(self, field: str, value: Any, order_by: str = "id") -> List[Dict]:
        """根据字段查询"""
        return self.db.fetchall(
            f"SELECT * FROM {self.table_name} WHERE {field} = ? ORDER BY {order_by}",
            (value,)
        )

    def insert(self, data: Dict) -> int:
        """插入数据"""
        return self.db.insert(self.table_name, data)

    def update(self, id: int, data: Dict) -> int:
        """更新数据"""
        return self.db.update(self.table_name, data, "id = ?", (id,))

    def delete(self, id: int) -> int:
        """删除数据"""
        return self.db.delete(self.table_name, "id = ?", (id,))

    def count(self) -> int:
        """统计记录总数"""
        result = self.db.fetchone(f"SELECT COUNT(*) as cnt FROM {self.table_name}")
        return result.get('cnt', 0) if result else 0

    def exists(self, id: int) -> bool:
        """检查记录是否存在"""
        result = self.db.fetchone(
            f"SELECT COUNT(*) as cnt FROM {self.table_name} WHERE id = ?",
            (id,)
        )
        return result.get('cnt', 0) > 0 if result else False
