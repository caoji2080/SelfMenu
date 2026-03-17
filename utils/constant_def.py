"""
常量定义 - 应用中使用的各种常量
"""

# 菜谱状态常量
class RecipeStatus:
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

    @staticmethod
    def get_label(status: str) -> str:
        labels = {
            RecipeStatus.DRAFT: '草稿',
            RecipeStatus.PUBLISHED: '已发布',
            RecipeStatus.ARCHIVED: '已归档'
        }
        return labels.get(status, status)

    @staticmethod
    def get_icon(status: str) -> str:
        icons = {
            RecipeStatus.DRAFT: '📝',
            RecipeStatus.PUBLISHED: '✅',
            RecipeStatus.ARCHIVED: '🗄️'
        }
        return icons.get(status, '📄')


# 难度等级常量
class DifficultyLevel:
    EASY = '简单'
    MEDIUM = '中等'
    HARD = '困难'
    EXPERT = '专家'

    LEVELS = [EASY, MEDIUM, HARD, EXPERT]

    @staticmethod
    def get_stars(level: str) -> str:
        stars_map = {
            DifficultyLevel.EASY: '⭐',
            DifficultyLevel.MEDIUM: '⭐⭐',
            DifficultyLevel.HARD: '⭐⭐⭐',
            DifficultyLevel.EXPERT: '⭐⭐⭐⭐'
        }
        return stars_map.get(level, '⭐')


# 时间单位常量
class TimeUnit:
    MINUTES = '分钟'
    HOURS = '小时'

    @staticmethod
    def format_time(minutes: int) -> str:
        """格式化时间显示"""
        if minutes < 60:
            return f"{minutes}分钟"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}小时{mins}分钟" if mins > 0 else f"{hours}小时"


# 分享方式常量
class ShareMethod:
    WECHAT = '微信'
    QQ = 'QQ'
    EMAIL = '邮件'
    COPY_LINK = '复制链接'
    EXPORT_JSON = '导出 JSON'
    EXPORT_CSV = '导出 CSV'

    ALL = [WECHAT, QQ, EMAIL, COPY_LINK, EXPORT_JSON, EXPORT_CSV]


# 导出格式常量
class ExportFormat:
    JSON = 'json'
    CSV = 'csv'
    TXT = 'txt'

    ALL = [JSON, CSV, TXT]


# 消息类型常量
class MessageType:
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'


# UI 颜色常量
class UIColors:
    PRIMARY = '#2196F3'      # 蓝色
    SUCCESS = '#4CAF50'      # 绿色
    WARNING = '#FF9800'      # 橙色
    ERROR = '#F44336'        # 红色
    INFO = '#00BCD4'         # 青色
    TEXT_PRIMARY = '#333333' # 深灰
    TEXT_SECONDARY = '#666666'  # 中灰
    BACKGROUND = '#FFFFFF'   # 白色
    BACKGROUND_ALT = '#F5F5F5'  # 浅灰


# 字体常量
class UIFonts:
    TITLE_FAMILY = 'Arial'
    CONTENT_FAMILY = 'Microsoft YaHei'

    TITLE_SIZE = 28
    HEADING_SIZE = 18
    SUBHEADING_SIZE = 14
    CONTENT_SIZE = 12
    SMALL_SIZE = 10


# 间距常量
class UISpacing:
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 15
    PADDING_XLARGE = 20


# 数据库表名常量
class TableNames:
    RECIPES = 'recipes'
    CATEGORIES = 'categories'
    SHARES = 'shares'
    TAGS = 'tags'
    RECIPE_TAGS = 'recipe_tags'
