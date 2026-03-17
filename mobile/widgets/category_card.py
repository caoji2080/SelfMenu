# 文件名：mobile/widgets/category_card.py
# 参考名称：09_类别卡片组件
# 说明：展示类别信息的卡片组件

import flet as ft


class CategoryCard(ft.Container):
    """类别卡片 - 用于类别管理"""

    def __init__(self, category, on_edit=None, on_delete=None):
        super().__init__()
        self.category = category
        self.on_edit_callback = on_edit
        self.on_delete_callback = on_delete

        self.content = self._build_card()
        self.padding = 15
        self.border_radius = 10
        self.bgcolor = ft.colors.WHITE
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.BLACK12,
        )

    def _build_card(self):
        """构建卡片内容"""
        return ft.Row(
            controls=[
                ft.Text(
                    self.category.icon or '🏷️',
                    size=40,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            self.category.name,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            self.category.description or "",
                            size=12,
                            color=ft.colors.GREY_600,
                        ),
                    ],
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    on_click=self._handle_edit,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    on_click=self._handle_delete,
                    icon_color=ft.colors.RED,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _handle_edit(self, e):
        """处理编辑事件"""
        if self.on_edit_callback:
            self.on_edit_callback(e)

    def _handle_delete(self, e):
        """处理删除事件"""
        if self.on_delete_callback:
            self.on_delete_callback(e)
