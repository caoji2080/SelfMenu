
"""
分享数据持久化操作
"""
from typing import List, Dict, Optional
from repositories.base_repository import BaseRepository

class ShareRepository(BaseRepository):
    """分享数据仓库类"""

    table_name = "shares"

    def __init__(self):
        super().__init__()

    def find_by_recipe(self, recipe_id: int) -> List[Dict]:
        """根据菜谱查询分享记录"""
        sql = """
            SELECT s.*, r.title as recipe_title 
            FROM shares s 
            LEFT JOIN recipes r ON s.recipe_id = r.id 
            WHERE s.recipe_id = ? 
            ORDER BY s.shared_at DESC
        """
        return self.db.fetchall(sql, (recipe_id,))

    def find_recent(self, limit: int = 10) -> List[Dict]:
        """查询最近的分享记录"""
        sql = """
            SELECT s.*, r.title as recipe_title 
            FROM shares s 
            LEFT JOIN recipes r ON s.recipe_id = r.id 
            ORDER BY s.shared_at DESC 
            LIMIT ?
        """
        return self.db.fetchall(sql, (limit,))

    def find_by_method(self, share_method: str) -> List[Dict]:
        """根据分享方式查询记录"""
        sql = """
            SELECT s.*, r.title as recipe_title 
            FROM shares s 
            LEFT JOIN recipes r ON s.recipe_id = r.id 
            WHERE s.share_method = ? 
            ORDER BY s.shared_at DESC
        """
        return self.db.fetchall(sql, (share_method,))

    def get_statistics(self) -> Dict:
        """获取分享统计信息"""
        sql = """
            SELECT 
                COUNT(*) as total_shares,
                share_method,
                COUNT(*) as method_count
            FROM shares 
            GROUP BY share_method
            ORDER BY method_count DESC
        """
        return self.db.fetchall(sql)

    def count_by_recipe(self, recipe_id: int) -> int:
        """统计某个菜谱的分享次数"""
        result = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM shares WHERE recipe_id = ?",
            (recipe_id,)
        )
        return result.get('cnt', 0) if result else 0
