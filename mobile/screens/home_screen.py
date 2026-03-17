# 文件名：mobile/screens/home_screen.py
# 目录：mobile/screens/home_screen.py
# 功能：应用首页 - 显示欢迎信息、快捷操作和统计信息

import flet as ft
from datetime import datetime


class HomeScreen(ft.Container):
    """主屏幕 - 应用首页"""

    def __init__(self, on_navigate, recipe_service, category_service):
        super().__init__()
        self.on_navigate = on_navigate
        self.recipe_service = recipe_service
        self.category_service = category_service
        self.recipe_count = 0
        self.category_count = 0
        self.favorite_count = 0
        self.recent_recipes = []
        self.expand = True

        # 直接在__init__中构建 UI
        self.content = self._build_ui()

    def _build_ui(self):
        """构建 UI"""
        # 获取统计数据
        try:
            all_recipes = self.recipe_service.get_all_recipes()
            all_categories = self.category_service.get_all_categories()
            self.recipe_count = len(all_recipes)
            self.category_count = len(all_categories)
            # TODO: 收藏功能待实现
            self.favorite_count = 0

            # 获取最近更新的菜谱（按更新时间倒序排列，取前 2 个）
            if all_recipes:
                # 假设有 updated_at 字段，按更新时间排序
                sorted_recipes = sorted(
                    all_recipes,
                    key=lambda r: r.updated_at or r.created_at or '',
                    reverse=True
                )
                self.recent_recipes = sorted_recipes[:2]
            else:
                self.recent_recipes = []
        except Exception as e:
            print(f"⚠️ 获取数据失败：{e}")
            self.recipe_count = 0
            self.category_count = 0
            self.favorite_count = 0
            self.recent_recipes = []

        hour = datetime.now().hour
        greeting = "早上好" if hour < 12 else ("下午好" if hour < 18 else "晚上好")

        return ft.Column(
            controls=[
                # 顶部栏
                ft.Container(
                    content=ft.Row([
                        ft.Text("🍳", size=32),
                        ft.Text("个人菜谱管理系统", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ], alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                    bgcolor="#FF6B6B",
                    border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
                ),

                # 欢迎区域
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{greeting}！", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                        ft.Text(
                            f"📅 {datetime.now().strftime('%Y年%m月%d日 %A')}",
                            size=14,
                            color=ft.colors.GREY_700,
                        ),
                    ], spacing=5),
                    padding=20,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#FFE5E5", "#FFF0F0"],
                    ),
                    border_radius=15,
                    margin=ft.margin.symmetric(horizontal=15, vertical=10),
                ),

                # 统计卡片（添加点击事件）
                ft.Container(
                    content=ft.Row([
                        self._create_stat_card("📚", "菜谱总数", str(self.recipe_count), "#E3F2FD", "/recipes"),
                        self._create_stat_card("🏷️", "类别数量", str(self.category_count), "#E8F5E9", "/categories"),
                        self._create_stat_card("⭐", "收藏菜谱", str(self.favorite_count), "#FFF3E0", "/favorites"),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=15,
                    margin=ft.margin.symmetric(horizontal=15, vertical=5),
                ),

                # 快捷操作标题
                ft.Container(
                    content=ft.Text("快捷操作", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    padding=ft.padding.only(left=15, top=10, bottom=5),
                ),

                # 快捷操作按钮
                ft.Container(
                    content=ft.Row([
                        self._create_action_button("📝", "新建菜谱", "/new_recipe"),
                        self._create_action_button("🔍", "搜索菜谱", "/search"),
                        self._create_action_button("🏷️", "类别管理", "/categories"),
                        self._create_action_button("📤", "导入导出", "/import_export"),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=15,
                ),

                # 最近更新的菜谱标题
                ft.Container(
                    content=ft.Row([
                        ft.Text("最近更新的菜谱", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                        ft.TextButton(
                            "查看全部 >",
                            on_click=lambda e: self.on_navigate("/recipes"),
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.only(left=15, top=10, bottom=5),
                ),

                # 最近更新的菜谱列表
                self._create_recent_recipes_list(),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
        )

    def _create_recent_recipes_list(self):
        """创建最近更新的菜谱列表"""
        if not self.recent_recipes:
            # 空状态
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.RESTAURANT_MENU, size=60, color=ft.colors.GREY_400),
                    ft.Text("暂无菜谱数据", size=14, color=ft.colors.GREY_600),
                    ft.Text("点击\"新建菜谱\"开始创建你的第一个菜谱吧！", size=12, color=ft.colors.GREY_500),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=40,
                bgcolor=ft.colors.GREY_100,
                border_radius=10,
                margin=ft.margin.symmetric(horizontal=15, vertical=5),
            )

        # 创建菜谱列表
        recipe_cards = []
        for recipe in self.recent_recipes:
            card = self._create_recent_recipe_card(recipe)
            recipe_cards.append(card)

        return ft.Container(
            content=ft.Column(
                controls=recipe_cards,
                spacing=10,
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
        )

    def _create_recent_recipe_card(self, recipe):
        """创建单个菜谱卡片"""
        # 格式化更新时间
        update_time = recipe.updated_at or recipe.created_at or '未知'
        if len(update_time) > 16:
            update_time = update_time[:16].replace('T', ' ')

        return ft.Container(
            content=ft.Row([
                # 左侧编号
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"#{recipe.id}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    width=50,
                    alignment=ft.alignment.center,
                ),
                # 中间信息
                ft.Container(
                    content=ft.Column([
                        ft.Text(recipe.title, size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                        ft.Row([
                            ft.Icon(ft.icons.LABEL_OUTLINE, size=14, color=ft.colors.GREY_600),
                            ft.Text(recipe.category_name or "未分类", size=12, color=ft.colors.GREY_600),
                            ft.VerticalDivider(width=1, color=ft.colors.GREY_400),
                            ft.Icon(ft.icons.UPDATE, size=14, color=ft.colors.GREY_600),
                            ft.Text(update_time, size=12, color=ft.colors.GREY_600),
                        ], spacing=5),
                    ], spacing=5),
                    expand=True,
                    padding=ft.padding.only(right=10),
                ),
                # 右侧箭头
                ft.Icon(ft.icons.CHEVRON_RIGHT, color=ft.colors.GREY_400),
            ], alignment=ft.MainAxisAlignment.START),
            padding=15,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            on_click=lambda e, r=recipe: self.on_recipe_click(r),
            ink=True,
        )

    def on_recipe_click(self, recipe):
        """点击菜谱时的处理"""
        route = f"/recipe/{recipe.id}"
        print(f"🔍 点击最近更新的菜谱，路由：{route}, recipe_id={recipe.id}")
        self.on_navigate(route, recipe_id=recipe.id)

    def _create_stat_card(self, icon: str, label: str, value: str, bgcolor: str, navigate_route: str):
        """创建统计卡片（带点击事件）"""
        return ft.Container(
            content=ft.Column([
                ft.Text(icon, size=28),
                ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                ft.Text(label, size=12, color=ft.colors.GREY_700),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=15,
            bgcolor=bgcolor,
            border_radius=10,
            width=100,
            on_click=lambda e: self._handle_stat_click(navigate_route),
            ink=True,  # 添加水波纹效果
        )

    def _handle_stat_click(self, route: str):
        """处理统计卡片点击"""
        print(f"📊 点击统计卡片，路由：{route}")

        # 特殊处理收藏菜谱路由（如果路由是 /favorites，但目前没有这个页面，先跳转到菜谱列表）
        if route == "/favorites":
            # TODO: 收藏功能待实现，暂时显示提示
            print("⚠️ 收藏功能尚未实现")
            # 可以添加一个提示框
            return

        self.on_navigate(route)

    def _create_action_button(self, icon: str, label: str, route: str):
        """创建快捷操作按钮"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(icon, size=32),
                    padding=15,
                    bgcolor=ft.colors.GREY_200,
                    border_radius=50,
                    width=70,
                    height=70,
                    alignment=ft.alignment.center,
                ),
                ft.Text(label, size=12, color=ft.colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            on_click=lambda e: self.on_navigate(route),
            padding=10,
            width=90,
        )

    def did_mount(self):
        """组件挂载后更新页面配置"""
        print("✅ 菜谱主界面构建完成")
