# 文件名：mobile/app.py
# 目录：mobile/app.py
# 功能：MenuApp 主类 - 管理所有屏幕和导航，统一处理页面切换和顶部 AppBar

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径（确保能导入 models、services、repositories）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from mobile.screens.home_screen import HomeScreen
from mobile.screens.recipe_list_screen import RecipeListScreen
from mobile.screens.recipe_form_screen import RecipeFormScreen
from mobile.screens.recipe_detail_screen import RecipeDetailScreen
from mobile.screens.search_screen import SearchScreen
from mobile.screens.category_screen import CategoryScreen
from mobile.screens.import_export_screen import ImportExportScreen

# 导入真实的服务层
from services.recipe_service import RecipeService
from services.category_service import CategoryService


class MenuApp(ft.Column):
    """菜谱应用主类 - 管理所有屏幕和导航"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.expand = True
        self.page = page
        self.current_route = "/"

        # 配置页面
        page.title = "个人菜谱管理系统"
        page.bgcolor = "#F7F7F7"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        # 创建真实的 service 对象（连接到数据库）
        self.recipe_service = RecipeService()
        self.category_service = CategoryService()

        # 初始化所有屏幕
        self.screens = {}
        self._init_screens()

        # 显示首页
        self.controls = [self.screens["/"]]

    def _init_screens(self):
        """初始化所有屏幕"""
        # 首页
        self.screens["/"] = HomeScreen(
            on_navigate=self.navigate_to,
            recipe_service=self.recipe_service,
            category_service=self.category_service
        )

        # 菜谱列表页
        self.screens["/recipes"] = RecipeListScreen(
            page=self.page,
            on_navigate=self.navigate_to,
            recipe_service=self.recipe_service
        )

        # 新建/编辑菜谱页（先初始化，参数在导航时设置）
        self.screens["/new_recipe"] = RecipeFormScreen(
            page=self.page,
            on_navigate=self.navigate_to,
            recipe_service=self.recipe_service,
            category_service=self.category_service,
            is_edit=False,  # 默认新建模式
            recipe_id=None
        )

        # 菜谱详情页（先初始化，recipe_id 在导航时设置）
        self.screens["/recipe/:id"] = RecipeDetailScreen(
            page=self.page,
            on_navigate=self.navigate_to,
            recipe_service=self.recipe_service
        )

        # 搜索页（直接传入 category_service）
        self.screens["/search"] = SearchScreen(
            page=self.page,
            on_navigate=self.navigate_to,
            recipe_service=self.recipe_service,
            category_service=self.category_service
        )

        # 类别管理页
        self.screens["/categories"] = CategoryScreen(
            page=self.page,
            on_navigate=self.navigate_to,
            category_service=self.category_service
        )

        # 导入导出页
        self.screens["/import_export"] = ImportExportScreen(
            page=self.page,
            on_navigate=self.navigate_to,
            recipe_service=self.recipe_service
        )

        # 收藏菜谱页（暂时用菜谱列表页代替，后续可实现真正的收藏功能）
        self.screens["/favorites"] = RecipeListScreen(
            page=self.page,
            on_navigate=self.navigate_to,
            recipe_service=self.recipe_service
        )

    def navigate_to(self, route: str, **kwargs):
        """导航到指定页面"""
        print(f"🧭 导航：{route}")
        print(f"📦 参数：{kwargs}")

        # 处理动态路由（如 /recipe/1）
        target_screen = None
        matched_route_pattern = None
        recipe_id = None

        # 检查是否是详情页路由（匹配 /recipe/* 格式）
        if route.startswith("/recipe/"):
            # 提取 recipe_id
            parts = route.split("/")
            if len(parts) >= 3:
                recipe_id = parts[2]  # 获取实际的 ID，如 "1"
                print(f"📋 提取 recipe_id: {recipe_id}")

                # 设置详情页的 recipe_id
                detail_screen = self.screens.get("/recipe/:id")
                if detail_screen:
                    detail_screen.recipe_id = recipe_id
                    print(f"✅ 已设置 detail_screen.recipe_id = {recipe_id}")

        # 查找匹配的屏幕
        for route_pattern, screen in self.screens.items():
            if route_pattern == route:
                target_screen = screen
                matched_route_pattern = route_pattern
                break
            elif route_pattern == "/recipe/:id" and route.startswith("/recipe/"):
                target_screen = screen
                matched_route_pattern = route_pattern
                break

        # 如果找到对应的屏幕
        if target_screen:
            # 处理编辑模式的参数传递
            if matched_route_pattern == "/new_recipe":
                # 更新表单屏幕的参数
                form_screen = self.screens["/new_recipe"]
                if kwargs.get('is_edit'):
                    form_screen.is_edit = True
                    form_screen.recipe_id = kwargs.get('recipe_id')
                    print(f"✅ 设置为编辑模式，recipe_id={form_screen.recipe_id}")
                else:
                    form_screen.is_edit = False
                    form_screen.recipe_id = None
                    print(f"✅ 设置为新建模式")

            # 根据路由设置 AppBar
            self._setup_appbar(route, target_screen)

            # 清除当前控件并添加新屏幕
            self.controls.clear()
            self.controls.append(target_screen)
            self.page.update()

            # 调用 did_mount 加载数据
            if hasattr(target_screen, 'did_mount'):
                target_screen.did_mount()

            print(f"✅ 已导航到：{route}")
        else:
            print(f"⚠️ 未找到路由：{route}")
            # 默认返回首页
            self.navigate_to("/")

    def _setup_appbar(self, route: str, screen):
        """根据路由设置顶部 AppBar"""
        appbar_config = {
            "/": {"title": "个人菜谱管理系统", "show_back": False},
            "/recipes": {"title": "菜谱列表", "show_back": True},
            "/new_recipe": {"title": "新建菜谱", "show_back": True},
            "/recipe/:id": {"title": "菜谱详情", "show_back": True},
            "/search": {"title": "搜索菜谱", "show_back": True},
            "/categories": {"title": "类别管理", "show_back": True},
            "/import_export": {"title": "导入导出", "show_back": True},
            "/favorites": {"title": "收藏菜谱", "show_back": True},
        }

        config = appbar_config.get(route, {"title": "菜单", "show_back": True})

        if config["show_back"]:
            self.page.appbar = ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: self.navigate_to("/"),
                    icon_color=ft.colors.WHITE,
                ),
                title=ft.Text(config["title"]),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
        else:
            self.page.appbar = ft.AppBar(
                title=ft.Text(config["title"]),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
