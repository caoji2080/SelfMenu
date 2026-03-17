# 文件名：mobile/widgets/bottom_nav.py
# 参考名称：10_底部导航栏
# 说明：应用底部导航栏组件

import flet as ft


class BottomNavBar(ft.Container):
    """底部导航栏"""

    def __init__(self, on_navigate, current_route: str = "/home"):
        super().__init__()
        self.on_navigate = on_navigate
        self.current_route = current_route

        self.content = self._build_navbar()
        self.padding = 10
        self.bgcolor = ft.colors.WHITE
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.BLACK12,
        )

    def _build_navbar(self):
        """构建导航栏"""
        nav_items = [
            ("/", "🏠", "首页"),
            ("/recipes", "📚", "菜谱"),
            ("/search", "🔍", "搜索"),
            ("/categories", "🏷️", "类别"),
        ]

        return ft.Row(
            controls=[
                self._create_nav_item(route, icon, label)
                for route, icon, label in nav_items
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

    def _create_nav_item(self, route: str, icon: str, label: str):
        """创建导航项"""
        is_active = self.current_route == route

        return ft.TextButton(
            content=ft.Column(
                controls=[
                    ft.Text(icon, size=24),
                    ft.Text(label, size=12),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            on_click=lambda e: self.on_navigate(route),
            style=ft.ButtonStyle(
                bgcolor=(
                    ft.colors.BLUE_100 if is_active
                    else ft.colors.TRANSPARENT
                ),
            ),
        )
