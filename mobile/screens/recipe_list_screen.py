# 文件名：mobile/screens/recipe_list_screen.py
# 目录：mobile/screens/recipe_list_screen.py
# 功能：菜谱列表屏幕 - 显示菜谱列表，支持分页和筛选

import flet as ft
from mobile.widgets.recipe_card import RecipeCard


class RecipeListScreen(ft.Container):
    """菜谱列表屏幕"""

    def __init__(self, page: ft.Page, on_navigate, recipe_service, category_id=None):
        super().__init__()
        self._page = page
        self.on_navigate = on_navigate
        self.recipe_service = recipe_service
        self.category_id = category_id
        self.current_page = 1
        self.page_size = 10
        self.recipes = []
        self.expand = True

        # 初始化控件
        self.recipe_list_view = None

        # 构建界面
        self.content = self._build_screen()

    def _build_screen(self):
        """构建菜谱列表屏幕"""
        return ft.Column(
            controls=[
                self._create_filter_bar(),
                self._create_recipe_list(),
                self._create_pagination(),
            ],
            expand=True,
        )

    def _create_filter_bar(self):
        """创建筛选栏"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Dropdown(
                        label="按类别筛选",
                        options=[],
                        expand=True,
                        on_change=self.on_category_changed,
                    ),
                    ft.IconButton(
                        icon=ft.icons.SEARCH,
                        on_click=lambda e: self.on_navigate("/search"),
                    ),
                ],
            ),
            padding=10,
        )

    def _create_recipe_list(self):
        """创建菜谱列表"""
        self.recipe_list_view = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False,
        )
        return self.recipe_list_view

    def _create_pagination(self):
        """创建分页控件"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "上一页",
                        on_click=self.prev_page,
                        disabled=self.current_page == 1,
                    ),
                    ft.Text(f"第 {self.current_page} 页"),
                    ft.ElevatedButton(
                        "下一页",
                        on_click=self.next_page,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
        )

    def prev_page(self, e):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_recipes()

    def next_page(self, e):
        """下一页"""
        self.current_page += 1
        self.load_recipes()

    def on_category_changed(self, e):
        """类别改变时的处理"""
        self.current_page = 1
        self.load_recipes()

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
                title=ft.Text("菜谱列表"),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
            self._page.update()

        self.load_recipes()

    def load_recipes(self):
        """加载菜谱列表"""
        try:
            self.recipes = self.recipe_service.get_all_recipes(
                page=self.current_page,
                page_size=self.page_size
            )

            if self.recipe_list_view:
                self.recipe_list_view.controls.clear()

                for recipe in self.recipes:
                    card = RecipeCard(
                        recipe=recipe,
                        on_click=lambda e, r=recipe: self.on_recipe_click(r)
                    )
                    self.recipe_list_view.controls.append(card)

                self._page.update()
        except Exception as e:
            print(f"加载菜谱列表失败：{e}")

    def on_recipe_click(self, recipe):
        """点击菜谱时的处理 - 修复：传递实际的路由而不是模板"""
        # 构造正确的路由，如 /recipe/1
        route = f"/recipe/{recipe.id}"
        print(f"🔍 点击菜谱，路由：{route}, recipe_id={recipe.id}")
        self.on_navigate(route, recipe_id=recipe.id)
