# 文件名：mobile/screens/recipe_detail_screen.py
# 目录：mobile/screens/recipe_detail_screen.py
# 功能：菜谱详情屏幕 - 显示单个菜谱的详细信息

import flet as ft


class RecipeDetailScreen(ft.Container):
    """菜谱详情屏幕 - 展示菜谱完整信息"""

    def __init__(self, page: ft.Page, on_navigate, recipe_service, recipe_id=None):
        super().__init__()
        self._page = page
        self.on_navigate = on_navigate
        self.recipe_service = recipe_service
        self.recipe_id = recipe_id
        self.recipe = None
        self.expand = True

        # 初始显示加载状态
        self.content = ft.Container(
            content=ft.Text("加载中...", size=16),
            padding=20,
        )

    def _build_screen(self):
        """构建菜谱详情界面"""
        return ft.Column(
            controls=[
                self._create_recipe_content(),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _create_recipe_content(self):
        """创建菜谱内容区域"""
        if not self.recipe:
            return ft.Container(
                content=ft.Text("加载中...", size=16),
                padding=20,
            )

        return ft.Container(
            content=ft.Column(
                controls=[
                    self._create_header(),
                    self._create_info_section(),
                    self._create_ingredients_section(),
                    self._create_steps_section(),
                    self._create_action_buttons(),
                ],
                spacing=20,
            ),
            padding=20,
        )

    def _create_header(self):
        """创建标题区域"""
        return ft.Column(
            controls=[
                ft.Text(
                    self.recipe.title,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    controls=[
                        ft.Chip(
                            label=ft.Text(self.recipe.status, color=ft.colors.WHITE),
                            bgcolor=ft.colors.PRIMARY,
                        ),
                        ft.Chip(
                            label=ft.Text(f"难度：{self.recipe.difficulty}", color=ft.colors.WHITE),
                            bgcolor=ft.colors.BLUE,
                        ),
                    ],
                ),
            ],
            spacing=10,
        )

    def _create_info_section(self):
        """创建基本信息区域"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("基本信息", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"📝 {self.recipe.description or '暂无描述'}"),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.TIMER, size=20),
                            ft.Text(f"⏱️ {self.recipe.cooking_time or '未设置'}分钟"),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.PEOPLE, size=20),
                            ft.Text(f"👥 {self.recipe.servings or 0}人份"),
                        ],
                    ),
                ],
                spacing=10,
            ),
            padding=15,
            bgcolor=ft.colors.BLUE_GREY_100,
            border_radius=10,
        )

    def _create_ingredients_section(self):
        """创建食材区域 - 修复：处理字符串格式的食材"""
        # 如果 ingredients 是字符串，按换行符分割
        if isinstance(self.recipe.ingredients, str):
            ingredients_list = [line.strip() for line in self.recipe.ingredients.split('\n') if line.strip()]
        elif isinstance(self.recipe.ingredients, list):
            ingredients_list = self.recipe.ingredients
        else:
            ingredients_list = []

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("🛒 食材准备", size=18, weight=ft.FontWeight.BOLD),
                    *[ft.Text(f"• {item}", size=14) for item in ingredients_list],
                ],
                spacing=8,
            ),
            padding=15,
            bgcolor=ft.colors.BLUE_GREY_100,
            border_radius=10,
        )

    def _create_steps_section(self):
        """创建步骤区域 - 修复：处理字符串格式的步骤"""
        # 如果 steps 是字符串，按换行符分割
        if isinstance(self.recipe.steps, str):
            steps_list = [line.strip() for line in self.recipe.steps.split('\n') if line.strip()]
        elif isinstance(self.recipe.steps, list):
            steps_list = self.recipe.steps
        else:
            steps_list = []

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("👨‍ 制作步骤", size=18, weight=ft.FontWeight.BOLD),
                    *[
                        ft.Column(
                            controls=[
                                ft.Text(f"步骤 {i+1}", weight=ft.FontWeight.BOLD, size=14),
                                ft.Text(step, size=14),
                            ],
                            spacing=5,
                        )
                        for i, step in enumerate(steps_list)
                    ],
                ],
                spacing=15,
            ),
            padding=15,
            bgcolor=ft.colors.BLUE_GREY_100,
            border_radius=10,
        )

    def _on_edit_click(self, e):
        """编辑按钮点击事件"""
        print(f"✏️ 编辑按钮被点击，当前 recipe_id={self.recipe_id}")
        self.on_navigate("/new_recipe", recipe_id=self.recipe_id, is_edit=True)

    def _create_action_buttons(self):
        """创建操作按钮区域"""
        return ft.Row(
            controls=[
                ft.ElevatedButton(
                    "✏️ 编辑",
                    icon=ft.icons.EDIT,
                    on_click=self._on_edit_click,
                    expand=True,
                ),
                ft.ElevatedButton(
                    "🗑️ 删除",
                    icon=ft.icons.DELETE,
                    on_click=self.delete_recipe,
                    expand=True,
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                ),
            ],
            spacing=10,
        )

    def did_mount(self):
        """组件挂载后加载数据"""
        print(f"📱 RecipeDetailScreen.did_mount() 调用，recipe_id={self.recipe_id}")

        # 设置顶部 AppBar - 修复：返回按钮指向菜谱列表页
        if self._page:
            self._page.appbar = ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: self.on_navigate("/recipes"),  # 修改为返回列表页
                    icon_color=ft.colors.WHITE,
                ),
                title=ft.Text("菜谱详情"),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
            self._page.update()

        self.load_recipe()

    def load_recipe(self):
        """加载菜谱详情"""
        try:
            print(f"🔍 load_recipe() 开始加载，recipe_id={self.recipe_id}")

            if not self.recipe_id:
                print("⚠️ recipe_id 为空！")
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("错误：未指定菜谱 ID"),
                    bgcolor=ft.colors.RED,
                )
                self._page.snack_bar.open = True
                self._page.update()
                return

            # 尝试转换 recipe_id 为整数
            try:
                recipe_id_int = int(self.recipe_id)
            except (ValueError, TypeError):
                print(f"⚠️ recipe_id 转换失败：{self.recipe_id}")
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"错误：无效的菜谱 ID: {self.recipe_id}"),
                    bgcolor=ft.colors.RED,
                )
                self._page.snack_bar.open = True
                self._page.update()
                return

            print(f"✅ 使用 recipe_id={recipe_id_int} 查询数据库")
            self.recipe = self.recipe_service.get_recipe(recipe_id_int)

            if self.recipe:
                print(f"✅ 成功加载菜谱：{self.recipe.title}")
                print(f"📋 steps 类型：{type(self.recipe.steps)}, 值：{repr(self.recipe.steps[:100] if self.recipe.steps else None)}")

                # 关键修复：重新构建内容并调用 page.update()
                self.content = self._build_screen()
                print("🔄 重新构建内容完成")
                self._page.update()
                print("✅ 页面已更新")
            else:
                print(f"⚠️ 未找到菜谱 ID={recipe_id_int}")
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("未找到该菜谱"),
                    bgcolor=ft.colors.ORANGE,
                )
                self._page.snack_bar.open = True
                self._page.update()

        except Exception as e:
            print(f"❌ 加载菜谱详情失败：{e}")
            import traceback
            traceback.print_exc()
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"加载失败：{str(e)}"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()

    def delete_recipe(self, e):
        """删除菜谱"""
        print(f"🗑️ 删除按钮被点击，recipe_id={self.recipe_id}")

        dlg = ft.AlertDialog(
            title=ft.Text("确认删除"),
            content=ft.Text("确定要删除这个菜谱吗？"),
            actions=[
                ft.TextButton("取消", on_click=lambda e: self.close_dlg(dlg)),
                ft.TextButton("确定", on_click=lambda e: self.confirm_delete(dlg)),
            ],
        )
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def close_dlg(self, dlg):
        """关闭对话框"""
        dlg.open = False
        self._page.update()

    def confirm_delete(self, dlg):
        """确认删除"""
        try:
            print(f"🔍 开始删除菜谱，ID={self.recipe_id}")

            # 检查 recipe_id 是否存在
            if not self.recipe_id:
                print("❌ recipe_id 为空")
                raise Exception("菜谱 ID 为空")

            # 尝试转换为整数
            try:
                recipe_id_int = int(self.recipe_id)
            except (ValueError, TypeError) as ex:
                print(f"❌ recipe_id 转换失败：{self.recipe_id}, 错误：{ex}")
                raise Exception(f"无效的菜谱 ID: {self.recipe_id}")

            print(f"✅ 调用 recipe_service.delete_recipe({recipe_id_int})")
            success, msg = self.recipe_service.delete_recipe(recipe_id_int)

            if success:
                print(f"✅ 删除成功：{msg}")
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ 菜谱已删除"),
                    bgcolor=ft.colors.GREEN,
                )
                self._page.snack_bar.open = True
                self._page.update()

                # 延迟跳转到列表页
                import threading
                threading.Timer(1.0, lambda: self.on_navigate("/recipes")).start()
            else:
                print(f"❌ 删除失败：{msg}")
                raise Exception(msg)
        except Exception as e:
            print(f"❌ 删除过程异常：{e}")
            import traceback
            traceback.print_exc()
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 删除失败：{str(e)}"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()
        finally:
            dlg.open = False
            self._page.update()
