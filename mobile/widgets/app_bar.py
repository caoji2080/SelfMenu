# 文件名：mobile/widgets/app_bar.py
# 参考名称：11_顶部应用栏
# 说明：自定义顶部导航栏

import flet as ft


class CustomAppBar(ft.Container):
    """自定义顶部应用栏"""

    def __init__(self, title: str, show_back: bool = False, on_back=None):
        super().__init__()

        controls = []

        if show_back:
            controls.append(
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=on_back,
                    icon_size=24,
                ),
            )

        controls.append(
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
        )

        self.content = ft.Row(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
        )

        self.padding = ft.padding.all(15)
        self.bgcolor = ft.colors.PRIMARY
        self.color = ft.colors.WHITE
