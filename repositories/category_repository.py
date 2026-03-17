
"""
类别数据持久化操作
"""
from typing import List, Dict, Optional
from repositories.base_repository import BaseRepository

class CategoryRepository(BaseRepository):
    """类别数据仓库类"""

    table_name = "categories"

    def __init__(self):
        super().__init__()

    def find_all_with_count(self) -> List[Dict]:
        """查询所有类别（带菜谱数量统计）"""
        sql = """
            SELECT c.*, COUNT(r.id) as recipe_count 
            FROM categories c 
            LEFT JOIN recipes r ON c.id = r.category_id 
            GROUP BY c.id 
            ORDER BY c.sort_order, c.name
        """
        return self.db.fetchall(sql)

    def find_by_name(self, name: str) -> Optional[Dict]:
        """根据名称查询类别"""
        return self.db.fetchone(
            "SELECT * FROM categories WHERE name = ?",
            (name,)
        )

    def get_or_create(self, name: str, description: str = "", icon: str = "🍽️") -> int:
        """获取类别 ID，如果不存在则创建"""
        existing = self.find_by_name(name)
        if existing:
            return existing['id']

        return self.insert({
            'name': name,
            'description': description,
            'icon': icon,
            'sort_order': self.count()
        })

    def update_sort_order(self, category_id: int, sort_order: int) -> bool:
        """更新排序顺序"""
        try:
            self.db.execute(
                "UPDATE categories SET sort_order = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (sort_order, category_id)
            )
            return True
        except:
            return False

    def swap_sort_order(self, id1: int, id2: int) -> bool:
        """交换两个类别的排序顺序"""
        try:
            cat1 = self.find_by_id(id1)
            cat2 = self.find_by_id(id2)

            if cat1 and cat2:
                self.update_sort_order(id1, cat2['sort_order'])
                self.update_sort_order(id2, cat1['sort_order'])
                return True
            return False
        except:
            return False

    def has_recipes(self, category_id: int) -> bool:
        """检查类别下是否有菜谱"""
        result = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM recipes WHERE category_id = ?",
            (category_id,)
        )
        return result.get('cnt', 0) > 0 if result else False

    def get_empty_categories(self) -> List[Dict]:
        """获取没有菜谱的类别"""
        sql = """
            SELECT c.* FROM categories c 
            LEFT JOIN recipes r ON c.id = r.category_id 
            WHERE r.id IS NULL
        """
        return self.db.fetchall(sql)
