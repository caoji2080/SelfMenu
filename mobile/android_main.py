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
    try:
        # 配置页面
        page.title = "个人菜谱管理系统"
        page.bgcolor = "#F7F7F7"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        print("🚀 正在初始化应用...")

        # 创建应用实例
        app = MenuApp(page)
        page.add(app)
        page.update()

        print("✅ 应用加载成功")

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"❌ 应用加载失败：{e}")
        print(f"错误详情：{error_msg}")

        # 显示错误信息给用户
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("应用启动失败", size=20, weight="bold"),
                    ft.Text(f"错误：{str(e)}", color=ft.colors.RED),
                    ft.Text("请检查日志或重新安装", size=12),
                ]),
                padding=20,
            )
        )
        page.update()


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)
