# 文件名：mobile/config/settings.py
# 参考名称：00_应用配置文件
# 说明：应用配置和常量定义

from pathlib import Path

# 应用基础信息
APP_NAME = "个人菜谱管理系统"
APP_VERSION = "1.0.0"
APP_ICON = "🍳"

# 主题颜色
PRIMARY_COLOR = "#FF6B6B"
SECONDARY_COLOR = "#4ECDC4"
ACCENT_COLOR = "#FFE66D"
BG_COLOR = "#F7F7F7"
CARD_BG_COLOR = "#FFFFFF"

# 分页配置
PAGE_SIZE = 10

# 默认类别
DEFAULT_CATEGORIES = [
    {'name': '中餐', 'icon': '🍜', 'description': '中式菜肴'},
    {'name': '西餐', 'icon': '🍝', 'description': '西式菜肴'},
    {'name': '甜点', 'icon': '🍰', 'description': '甜品点心'},
    {'name': '饮品', 'icon': '🥤', 'description': '饮料饮品'},
    {'name': '沙拉', 'icon': '🥗', 'description': '沙拉轻食'},
    {'name': '汤品', 'icon': '🍲', 'description': '汤类菜品'},
    {'name': '快餐', 'icon': '🍔', 'description': '快捷简餐'},
]

# 菜谱状态
RECIPE_STATUS = {
    'draft': '草稿',
    'published': '已发布',
    'archived': '已归档'
}

# 难度等级
DIFFICULTY_LEVELS = ['简单', '中等', '困难', '专家']

# UI 配置
CARD_BORDER_RADIUS = 10
CARD_ELEVATION = 2
BUTTON_HEIGHT = 45
INPUT_HEIGHT = 50
