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
APP_NAME = "Recipe Manager"
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

# Category Icons (Unicode escape sequences)
CATEGORY_ICONS = {
    'Chinese': '\\u{1f35c}',
    'Western': '\\u{1f35d}',
    'Dessert': '\\u{1f370}',
    'Drink': '\\u{1f964}',
    'Salad': '\\u{1f957}',
    'Soup': '\\u{1f372}',
    'Fast Food': '\\u{1f354}',
    'Other': '\\u{1f37d}'
}

# Default Categories
DEFAULT_CATEGORIES = [
    {'name': 'Chinese', 'icon': '\\u{1f35c}', 'description': 'Chinese cuisine'},
    {'name': 'Western', 'icon': '\\u{1f35d}', 'description': 'Western cuisine'},
    {'name': 'Dessert', 'icon': '\\u{1f370}', 'description': 'Desserts and pastries'},
    {'name': 'Drink', 'icon': '\\u{1f964}', 'description': 'Beverages and drinks'},
    {'name': 'Salad', 'icon': '\\u{1f957}', 'description': 'Salads and light meals'},
    {'name': 'Soup', 'icon': '\\u{1f372}', 'description': 'Soups and stews'},
    {'name': 'Fast Food', 'icon': '\\u{1f354}', 'description': 'Quick meals and snacks'},
]
