# 文件名：mobile/utils/formatters.py
# 参考名称：15_格式化工具
# 说明：数据格式化辅助工具

from datetime import datetime


class Formatters:
    """格式化工具类"""

    @staticmethod
    def format_date(date_obj, format_str="%Y-%m-%d"):
        """格式化日期"""
        if not date_obj:
            return ""
        return date_obj.strftime(format_str)

    @staticmethod
    def format_datetime(date_obj, format_str="%Y-%m-%d %H:%M"):
        """格式化日期时间"""
        if not date_obj:
            return ""
        return date_obj.strftime(format_str)

    @staticmethod
    def format_time(minutes):
        """格式化时间（分钟转为可读格式）"""
        if not minutes:
            return "未设置"

        hours = minutes // 60
        mins = minutes % 60

        if hours > 0:
            return f"{hours}小时{mins}分钟"
        else:
            return f"{mins}分钟"

    @staticmethod
    def format_servings(servings):
        """格式化份量"""
        if not servings:
            return "未设置"
        return f"{servings}人份"

    @staticmethod
    def format_difficulty(difficulty):
        """格式化难度等级"""
        difficulty_map = {
            'simple': '简单',
            'medium': '中等',
            'hard': '困难',
            'expert': '专家'
        }
        return difficulty_map.get(difficulty, difficulty)

    @staticmethod
    def format_status(status):
        """格式化菜谱状态"""
        status_map = {
            'draft': '草稿',
            'published': '已发布',
            'archived': '已归档'
        }
        return status_map.get(status, status)

    @staticmethod
    def truncate_text(text, max_length=50):
        """截断文本"""
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    @staticmethod
    def format_list(items, separator=", "):
        """格式化列表为字符串"""
        if not items:
            return ""
        return separator.join(str(item) for item in items)
