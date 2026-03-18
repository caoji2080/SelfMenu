"""
Application Configuration and Constants
"""
import os
from pathlib import Path
import sys


def get_db_path():
    """Get database path (Android compatible)"""
    # Only try to import jnius in Android environment
    if 'ANDROID_ARGUMENT' in os.environ or sys.platform == 'android':
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = PythonActivity.mActivity

            files_dir = context.getFilesDir().getAbsolutePath()
            db_dir = Path(files_dir) / "databases"
            db_dir.mkdir(parents=True, exist_ok=True)
            return db_dir / "menu_app.db"
        except Exception as e:
            print(f"Warning: Could not get Android path: {e}")

    # Fallback to default path
    DATA_DIR = Path(__file__).parent / "data"
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR / "menu_app.db"


# Application Info
APP_NAME = "Personal Recipe Management System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "MenuApp Team"

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Create directories only in non-Android environment
if 'ANDROID_ARGUMENT' not in os.environ and sys.platform != 'android':
    for directory in [DATA_DIR, BASE_DIR / "data" / "export", BASE_DIR / "data" / "import"]:
        directory.mkdir(exist_ok=True)

DB_PATH = get_db_path()
EXPORT_DIR = DATA_DIR / "export"
IMPORT_DIR = DATA_DIR / "import"

# Window Config
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# Pagination
PAGE_SIZE = 10

# Supported Formats
SUPPORTED_FORMATS = ['.json', '.csv', '.txt']

# Share Methods
SHARE_METHODS = ['WeChat', 'QQ', 'Email', 'Copy Link', 'Export File']

# Recipe Status
RECIPE_STATUS = {
    'draft': 'Draft',
    'published': 'Published',
    'archived': 'Archived'
}

# Difficulty Levels
DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard', 'Expert']

# Category Icons (Unicode)
CATEGORY_ICONS = {
    'Chinese': '\U0001F35C',
    'Western': '\U0001F35D',
    'Dessert': '\U0001F370',
    'Drink': '\U0001F964',
    'Salad': '\U0001F957',
    'Soup': '\U0001F372',
    'Fast Food': '\U0001F354',
    'Other': '\U0001F37D'
}

# Default Categories
DEFAULT_CATEGORIES = [
    {'name': 'Chinese', 'icon': '\U0001F35C', 'description': 'Chinese cuisine'},
    {'name': 'Western', 'icon': '\U0001F35D', 'description': 'Western cuisine'},
    {'name': 'Dessert', 'icon': '\U0001F370', 'description': 'Desserts and pastries'},
    {'name': 'Drink', 'icon': '\U0001F964', 'description': 'Beverages and drinks'},
    {'name': 'Salad', 'icon': '\U0001F957', 'description': 'Salads and light meals'},
    {'name': 'Soup', 'icon': '\U0001F372', 'description': 'Soups and stews'},
    {'name': 'Fast Food', 'icon': '\U0001F354', 'description': 'Quick meals and snacks'},
]
