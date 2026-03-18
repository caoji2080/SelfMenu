"""
应用配置和常量定义
"""
import os
from pathlib import Path
import platform


def get_db_path():
    """获取数据库路径（适配 Android）"""
    # 检测是否在 Android 环境
    try:
        # Android 环境检测
        from jnius import autoclass  # 如果能导入 jnius，说明在 Android 上
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        context = PythonActivity.mActivity

        # 使用应用私有目录
        files_dir = context.getFilesDir().getAbsolutePath()
        db_dir = Path(files_dir) / "databases"
        db_dir.mkdir(parents=True, exist_ok=True)
        return db_dir / "menu_app.db"
    except (ImportError, Exception):
        # 非 Android 环境，使用默认路径
        DATA_DIR = Path(__file__).parent / "data"
        DATA_DIR.mkdir(exist_ok=True)
        return DATA_DIR / "menu_app.db"


# 应用基础信息
APP_NAME = "个人菜谱管理系统"
APP_VERSION = "1.0.0"
APP_AUTHOR = "MenuApp Team"

# 路径配置
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# 确保基础目录存在（非 Android 环境）
try:
    from jnius import autoclass
except ImportError:
    # 只在非 Android 环境创建目录
    for directory in [DATA_DIR, BASE_DIR / "data" / "export", BASE_DIR / "data" / "import"]:
        directory.mkdir(exist_ok=True)

DB_PATH = get_db_path()
EXPORT_DIR = DATA_DIR / "export"
IMPORT_DIR = DATA_DIR / "import"

# 窗口配置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# 分页配置
PAGE_SIZE = 10

# 支持的文件格式
SUPPORTED_FORMATS = ['.json', '.csv', '.txt']

# 分享方式
SHARE_METHODS = ['微信', 'QQ', '邮件', '复制链接', '导出文件']

# 菜谱状态
RECIPE_STATUS = {
    'draft': '草稿',
    'published': '已发布',
    'archived': '已归档'
}

# 难度等级
DIFFICULTY_LEVELS = ['简单', '中等', '困难', '专家']

# 类别图标映射
CATEGORY_ICONS = {
    '中餐': '🍜',
    '西餐': '🍝',
    '甜点': '🍰',
    '饮品': '🥤',
    '沙拉': '🥗',
    '汤品': '🍲',
    '快餐': '🍔',
    '其他': '🍽️'
}

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
