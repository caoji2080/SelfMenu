# 文件名：mobile/widgets/recipe_card.py
# 参考名称：08_菜谱卡片组件
# 说明：展示菜谱信息的卡片组件

import flet as ft


class RecipeCard(ft.Container):
    """菜谱卡片 - 用于列表展示"""

    def __init__(self, recipe, on_click=None):
        super().__init__()
        self.recipe = recipe
        self.on_click_callback = on_click

        self.content = self._build_card()
        self.padding = 15
        self.border_radius = 10
        self.bgcolor = ft.colors.WHITE
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.BLACK12,
        )
        self.on_click = self._handle_click

    def _build_card(self):
        """构建卡片内容"""
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            self.recipe.title,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                        ),
                        ft.Chip(
                            label=ft.Text(self.recipe.status, size=12, color=ft.colors.WHITE),
                            bgcolor=ft.colors.PRIMARY,
                        ),
                    ],
                ),
                ft.Text(
                    self.recipe.description or "暂无描述",
                    size=14,
                    color=ft.colors.GREY_600,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.TIMER_OUTLINED, size=16, color=ft.colors.GREY),
                        ft.Text(f"{self.recipe.cooking_time or '?'}分钟", size=12),
                        ft.Container(width=10),
                        ft.Icon(ft.icons.RESTAURANT, size=16, color=ft.colors.GREY),
                        ft.Text(f"{self.recipe.difficulty or '简单'}", size=12),
                    ],
                    spacing=5,
                ),
            ],
            spacing=8,
        )

    def _handle_click(self, e):
        """处理点击事件"""
        if self.on_click_callback:
            self.on_click_callback(e)
