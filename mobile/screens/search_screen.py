# 文件名：mobile/screens/search_screen.py
# 目录：mobile/screens/search_screen.py
# 功能：搜索屏幕 - 菜谱搜索功能，支持关键字和高级搜索

import flet as ft
from mobile.widgets.recipe_card import RecipeCard


class SearchScreen(ft.Container):
    """搜索屏幕 - 菜谱搜索功能"""

    def __init__(self, page: ft.Page, on_navigate, recipe_service, category_service=None):
        super().__init__()
        self._page = page
        self.on_navigate = on_navigate
        self.recipe_service = recipe_service
        self.category_service = category_service
        self.search_results = []
        self.expand = True

        self.content = self._build_screen()

    def _build_screen(self):
        """构建搜索界面"""
        return ft.Column(
            controls=[
                self._create_search_bar(),
                self._create_advanced_filters(),
                self._create_results_area(),
            ],
            expand=True,
        )

    def _create_search_bar(self):
        """创建搜索栏"""
        self.search_field = ft.TextField(
            label="搜索关键字",
            hint_text="输入菜谱名称、食材等...",
            expand=True,
            on_submit=self.do_search,
            border_radius=10,
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    self.search_field,
                    ft.IconButton(
                        icon=ft.icons.SEARCH,
                        on_click=self.do_search,
                        icon_size=28,
                    ),
                ],
            ),
            padding=10,
        )

    def _create_advanced_filters(self):
        """创建高级筛选器"""
        self.category_filter = ft.Dropdown(
            label="类别",
            options=[],
            expand=True,
        )

        self.difficulty_filter = ft.Dropdown(
            label="难度",
            options=[
                ft.dropdown.Option("简单"),
                ft.dropdown.Option("中等"),
                ft.dropdown.Option("困难"),
                ft.dropdown.Option("专家"),
            ],
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("高级筛选", weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            self.category_filter,
                            self.difficulty_filter,
                        ],
                    ),
                    ft.ElevatedButton(
                        "应用筛选",
                        on_click=self.apply_filters,
                    ),
                ],
                spacing=10,
            ),
            padding=10,
        )

    def _create_results_area(self):
        """创建结果展示区域"""
        self.results_list = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=False,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("搜索结果", weight=ft.FontWeight.BOLD),
                    self.results_list,
                ],
                spacing=10,
            ),
            padding=10,
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
                title=ft.Text("搜索菜谱"),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
            self._page.update()

        self.load_categories()
        # 修改：页面加载时不自动显示菜谱，保持空状态
        # 只在用户点击搜索按钮时才显示

    def load_categories(self):
        """加载类别筛选选项"""
        try:
            if self.category_service:
                categories = self.category_service.get_all_categories()
                self.category_filter.options = [
                    ft.dropdown.Option(cat.name) for cat in categories
                ]
            self.update()
        except Exception as e:
            print(f"加载类别失败：{e}")

    def do_search(self, e=None):
        """执行搜索 - 修改：空关键字时显示所有菜谱"""
        keyword = self.search_field.value.strip() if self.search_field.value else ""

        try:
            if keyword:
                # 有关键字，执行关键字搜索
                print(f"🔍 搜索关键字：{keyword}")
                results = self.recipe_service.search_recipes(keyword)
            else:
                # 无关键字，显示所有菜谱
                print("📋 无搜索条件，显示所有菜谱")
                results = self.recipe_service.get_all_recipes()

            self.display_results(results)
        except Exception as e:
            print(f"❌ 搜索失败：{e}")
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"搜索失败：{str(e)}"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()

    def apply_filters(self, e):
        """应用筛选条件"""
        self.do_search()

    def display_results(self, results):
        """显示搜索结果"""
        self.results_list.controls.clear()

        if not results:
            self.results_list.controls.append(
                ft.Text("没有找到匹配的菜谱", color=ft.colors.GREY),
            )
        else:
            # 显示结果数量
            result_count = ft.Text(f"共找到 {len(results)} 个菜谱", size=14, color=ft.colors.BLUE_GREY_700)
            self.results_list.controls.append(result_count)

            for recipe in results:
                card = RecipeCard(
                    recipe=recipe,
                    on_click=lambda e, r=recipe: self.on_recipe_click(r),
                )
                self.results_list.controls.append(card)

        self._page.update()

    def on_recipe_click(self, recipe):
        """点击菜谱 - 修复：传递实际的 recipe_id 而不是路由模板"""
        # 构造正确的路由，如 /recipe/1
        route = f"/recipe/{recipe.id}"
        print(f"🔍 点击菜谱，路由：{route}, recipe_id={recipe.id}")
        self.on_navigate(route, recipe_id=recipe.id)
