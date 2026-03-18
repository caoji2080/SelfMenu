# 文件名：mobile/android_main.py
# 目录：D:\MenuApp\mobile\android_main.py
# 功能：Android Buildozer 应用入口 - 使用正确的 Flet Android 初始化方式

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from mobile.app import MenuApp


def main(page: ft.Page):
    """Android 应用入口函数"""
    page.title = "个人菜谱管理系统"
    page.bgcolor = "#F7F7F7"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    try:
        app = MenuApp(page)
        page.add(app)
        page.update()
        print("✅ App loaded successfully")
    except Exception as e:
        print(f"❌ Error loading app: {e}")
        page.add(ft.Text(f"Error: {e}", color=ft.colors.RED))
        page.update()


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)
