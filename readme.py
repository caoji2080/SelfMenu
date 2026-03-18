# 🍳 个人菜谱管理系统 - 占位文件

"""
这是一个占位文件，实际的 README 应该是 markdown 格式。
请查看 readme.md 获取完整文档。
"""

# 应用信息
APP_NAME = "Personal Recipe Management System"
VERSION = "1.0.0"

# 功能特性列表
FEATURES = [
    "Recipe Management - Complete CRUD operations",
    "Category Management - Flexible recipe categorization",
    "Advanced Search - Multi-condition search",
    "Share Feature - Multiple sharing options",
    "Import/Export - JSON/CSV format support",
    "Statistics - Real-time data display"
]

# 技术栈
TECH_STACK = {
    "desktop": "Python + Tkinter + Flet",
    "mobile": "Python + Flet + Buildozer",
    "database": "SQLite3",
    "architecture": "MVC Layered Architecture"
}

if __name__ == "__main__":
    print(f"{APP_NAME} v{VERSION}")
    print("Features:")
    for feature in FEATURES:
        print(f"  - {feature}")
