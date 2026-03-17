# 文件名：mobile/widgets/common_dialogs.py
# 参考名称：12_通用对话框
# 说明：通用的对话框组件

import flet as ft


class CommonDialogs:
    """通用对话框工具类"""

    @staticmethod
    def show_loading(page: ft.Page, message: str = "加载中..."):
        """显示加载对话框"""
        dlg = ft.AlertDialog(
            content=ft.Row(
                controls=[
                    ft.ProgressRing(),
                    ft.Text(message),
                ]
            ),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    @staticmethod
    def hide_loading(page: ft.Page):
        """隐藏加载对话框"""
        if page.dialog:
            page.dialog.open = False
            page.update()

    @staticmethod
    def show_confirm(page: ft.Page, title: str, content: str, on_confirm):
        """显示确认对话框"""
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("取消", on_click=lambda e: CommonDialogs.close_dialog(page, dlg)),
                ft.TextButton("确定", on_click=lambda e: CommonDialogs.confirm_action(page, dlg, on_confirm)),
            ],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    @staticmethod
    def show_info(page: ft.Page, title: str, content: str):
        """显示信息对话框"""
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("确定", on_click=lambda e: CommonDialogs.close_dialog(page, dlg)),
            ],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    @staticmethod
    def show_error(page: ft.Page, title: str, content: str):
        """显示错误对话框"""