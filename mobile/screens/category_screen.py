# 文件名：mobile/screens/category_screen.py
# 目录：mobile/screens/category_screen.py
# 功能：类别管理屏幕 - 管理菜谱类别的界面

import flet as ft
from mobile.widgets.category_card import CategoryCard


class CategoryScreen(ft.Container):
    """类别管理屏幕"""

    def __init__(self, page: ft.Page, on_navigate, category_service):
        super().__init__()
        self._page = page
        self.on_navigate = on_navigate
        self.category_service = category_service
        self.categories = []
        self.expand = True

        self.content = self._build_screen()

    def _build_screen(self):
        """构建类别管理界面"""
        return ft.Column(
            controls=[
                self._create_category_list(),
                self._create_add_button(),
            ],
            expand=True,
        )

    def _create_category_list(self):
        """创建类别列表"""
        self.category_list_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
        )
        return self.category_list_view

    def _create_add_button(self):
        """添加按钮"""
        return ft.Container(
            content=ft.FloatingActionButton(
                icon=ft.icons.ADD,
                on_click=self.add_category,
                bgcolor=ft.colors.PRIMARY,
            ),
            padding=20,
            alignment=ft.alignment.bottom_right,
        )

    def did_mount(self):
        """组件挂载后加载数据"""
        # 设置顶部 AppBar
        if self._page:
            self._page.appbar = ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: self.on_navigate("/"),
                    icon_color=ft.colors.WHITE,
                ),
                title=ft.Text("类别管理"),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
            self._page.update()

        self.load_categories()

    def load_categories(self):
        """加载类别列表"""
        try:
            self.categories = self.category_service.get_all_categories()

            if self.category_list_view:
                self.category_list_view.controls.clear()

                for category in self.categories:
                    card = CategoryCard(
                        category=category,
                        on_edit=lambda e, c=category: self.edit_category(c),
                        on_delete=lambda e, c=category: self.delete_category(c),
                    )
                    self.category_list_view.controls.append(card)

                self._page.update()
        except Exception as e:
            print(f"加载类别列表失败：{e}")

    def add_category(self, e):
        """添加类别"""
        dlg = ft.AlertDialog(
            title=ft.Text("添加类别"),
            content=ft.Column(
                controls=[
                    ft.TextField(label="名称", key="name"),
                    ft.TextField(label="图标", key="icon"),
                    ft.TextField(label="描述", key="description", multiline=True),
                ]
            ),
            actions=[
                ft.TextButton("取消", on_click=lambda e: self.close_dlg(dlg)),
                ft.TextButton("确定", on_click=lambda e: self.confirm_add(dlg)),
            ],
        )
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def close_dlg(self, dlg):
        """关闭对话框"""
        dlg.open = False
        self._page.update()

    def confirm_add(self, dlg):
        """确认添加"""
        name = dlg.content.controls[0].value
        icon = dlg.content.controls[1].value
        description = dlg.content.controls[2].value

        if not name:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ 请输入类别名称"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        try:
            category_data = {
                'name': name,
                'icon': icon or '🏷️',
                'description': description or '',
            }

            success, msg, cat_id = self.category_service.create_category(category_data)
            if success:
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ 类别已添加"),
                    bgcolor=ft.colors.GREEN,
                )
                self.load_categories()
            else:
                raise Exception(msg)
        except Exception as e:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 添加失败：{str(e)}"),
                bgcolor=ft.colors.RED,
            )
        finally:
            dlg.open = False
            self._page.update()

    def edit_category(self, category):
        """编辑类别"""
        dlg = ft.AlertDialog(
            title=ft.Text("编辑类别"),
            content=ft.Column(
                controls=[
                    ft.TextField(label="名称", value=category.name, key="name"),
                    ft.TextField(label="图标", value=category.icon, key="icon"),
                    ft.TextField(label="描述", value=category.description, key="description", multiline=True),
                ]
            ),
            actions=[
                ft.TextButton("取消", on_click=lambda e: self.close_dlg(dlg)),
                ft.TextButton("确定", on_click=lambda e: self.confirm_edit(dlg, category)),
            ],
        )
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def confirm_edit(self, dlg, category):
        """确认编辑"""
        name = dlg.content.controls[0].value
        icon = dlg.content.controls[1].value
        description = dlg.content.controls[2].value

        try:
            category_data = {
                'name': name,
                'icon': icon or '🏷️',
                'description': description or '',
            }

            success, msg = self.category_service.update_category(category.id, category_data)
            if success:
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ 类别已更新"),
                    bgcolor=ft.colors.GREEN,
                )
                self.load_categories()
            else:
                raise Exception(msg)
        except Exception as e:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 更新失败：{str(e)}"),
                bgcolor=ft.colors.RED,
            )
        finally:
            dlg.open = False
            self._page.update()

    def delete_category(self, category):
        """删除类别"""
        dlg = ft.AlertDialog(
            title=ft.Text("确认删除"),
            content=ft.Text(f"确定要删除类别 '{category.name}' 吗？"),
            actions=[
                ft.TextButton("取消", on_click=lambda e: self.close_dlg(dlg)),
                ft.TextButton("确定", on_click=lambda e: self.confirm_delete(dlg, category)),
            ],
        )
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def confirm_delete(self, dlg, category):
        """确认删除"""
        try:
            success, msg = self.category_service.delete_category(category.id)
            if success:
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ 类别已删除"),
                    bgcolor=ft.colors.GREEN,
                )
                self.load_categories()
            else:
                raise Exception(msg)
        except Exception as e:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 删除失败：{str(e)}"),
                bgcolor=ft.colors.RED,
            )
        finally:
            dlg.open = False
            self._page.update()
