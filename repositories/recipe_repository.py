"""
菜谱数据持久化操作
"""
from typing import List, Dict, Optional
from repositories.base_repository import BaseRepository
from utils.database import db

class RecipeRepository(BaseRepository):
    """菜谱数据仓库类"""

    table_name = "recipes"

    def __init__(self):
        super().__init__()

    def find_with_category(self, recipe_id: int) -> Optional[Dict]:
        """查询菜谱（带类别信息）"""
        sql = """
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            WHERE r.id = ?
        """
        return self.db.fetchone(sql, (recipe_id,))

    def find_all_with_category(self, limit: int = None, offset: int = None,
                               order_by: str = "created_at DESC") -> List[Dict]:
        """查询所有菜谱（带类别信息，支持分页）"""
        sql = f"""
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            ORDER BY {order_by}
        """

        if limit and offset is not None:
            sql += f" LIMIT {limit} OFFSET {offset}"

        return self.db.fetchall(sql)

    def find_by_category(self, category_id: int) -> List[Dict]:
        """根据类别查询菜谱"""
        sql = """
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            WHERE r.category_id = ? 
            ORDER BY r.created_at DESC
        """
        return self.db.fetchall(sql, (category_id,))

    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """关键词搜索（标题、描述、食材、标签）"""
        sql = """
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            WHERE r.title LIKE ? OR r.description LIKE ? 
               OR r.ingredients LIKE ? OR r.tags LIKE ?
            ORDER BY r.created_at DESC
        """
        search_term = f"%{keyword}%"
        return self.db.fetchall(sql, (search_term, search_term, search_term, search_term))

    def search_advanced(self, filters: Dict) -> List[Dict]:
        """高级搜索"""
        sql = """
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            WHERE 1=1
        """
        params = []

        if filters.get('category_id'):
            sql += " AND r.category_id = ?"
            params.append(filters['category_id'])

        if filters.get('difficulty'):
            sql += " AND r.difficulty = ?"
            params.append(filters['difficulty'])

        if filters.get('status'):
            sql += " AND r.status = ?"
            params.append(filters['status'])

        if filters.get('max_time'):
            sql += " AND r.cooking_time <= ?"
            params.append(filters['max_time'])

        if filters.get('keyword'):
            sql += " AND (r.title LIKE ? OR r.ingredients LIKE ?)"
            kw = f"%{filters['keyword']}%"
            params.extend([kw, kw])

        sql += " ORDER BY r.created_at DESC"

        return self.db.fetchall(sql, tuple(params)) if params else self.db.fetchall(sql)

    def find_by_status(self, status: str) -> List[Dict]:
        """根据状态查询菜谱"""
        return self.find_by_field('status', status)

    def increment_view_count(self, recipe_id: int) -> bool:
        """增加浏览次数"""
        try:
            self.db.execute(
                "UPDATE recipes SET view_count = view_count + 1 WHERE id = ?",
                (recipe_id,)
            )
            return True
        except:
            return False

    def update_rating(self, recipe_id: int, rating: float) -> bool:
        """更新评分"""
        try:
            self.db.execute(
                "UPDATE recipes SET rating = ? WHERE id = ?",
                (rating, recipe_id)
            )
            return True
        except:
            return False

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        sql = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'published' THEN 1 ELSE 0 END) as published_count,
                SUM(CASE WHEN status = 'draft' THEN 1 ELSE 0 END) as draft_count,
                AVG(rating) as avg_rating,
                SUM(view_count) as total_views
            FROM recipes
        """
        return self.db.fetchone(sql) or {}

    def get_recent_recipes(self, limit: int = 10) -> List[Dict]:
        """获取最近的菜谱"""
        sql = """
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            ORDER BY r.created_at DESC 
            LIMIT ?
        """
        return self.db.fetchall(sql, (limit,))

    def get_popular_recipes(self, limit: int = 10) -> List[Dict]:
        """获取最受欢迎的菜谱（按浏览量）"""
        sql = """
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            ORDER BY r.view_count DESC 
            LIMIT ?
        """
        return self.db.fetchall(sql, (limit,))
