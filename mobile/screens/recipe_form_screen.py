# 文件名：mobile/screens/recipe_form_screen.py
# 目录：mobile/screens/recipe_form_screen.py
# 功能：菜谱表单屏幕 - 用于新建或编辑菜谱的表单界面

import flet as ft


class RecipeFormScreen(ft.Container):
    """菜谱表单屏幕 - 新建或编辑菜谱"""

    def __init__(self, page: ft.Page, on_navigate, recipe_service, category_service,
                 is_edit=False, recipe_id=None):
        super().__init__()
        self._page = page
        self.on_navigate = on_navigate
        self.recipe_service = recipe_service
        self.category_service = category_service
        self.is_edit = is_edit
        self.recipe_id = recipe_id
        self.recipe = None
        self.categories = []
        self.expand = True

        # 表单控件
        self.title_field = None
        self.description_field = None
        self.category_dropdown = None
        self.ingredients_area = None
        self.steps_area = None
        self.cooking_time_field = None
        self.servings_field = None
        self.difficulty_dropdown = None
        self.status_dropdown = None

        # 构建界面
        self.content = self._build_screen()

    def _build_screen(self):
        """构建表单界面"""
        return ft.Column(
            controls=[
                self._create_form(),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _create_form(self):
        """创建表单"""
        self.title_field = ft.TextField(
            label="菜谱名称 *",
            border_radius=10,
        )

        self.description_field = ft.TextField(
            label="简介描述",
            multiline=True,
            min_lines=3,
            border_radius=10,
        )

        self.category_dropdown = ft.Dropdown(
            label="类别",
            options=[],
            border_radius=10,
        )

        self.ingredients_area = ft.TextField(
            label="食材清单（每行一个）",
            multiline=True,
            min_lines=5,
            border_radius=10,
        )

        self.steps_area = ft.TextField(
            label="制作步骤（每行一步）",
            multiline=True,
            min_lines=8,
            border_radius=10,
        )

        self.cooking_time_field = ft.TextField(
            label="烹饪时间（分钟）",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
        )

        self.servings_field = ft.TextField(
            label="份量（人）",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
        )

        self.difficulty_dropdown = ft.Dropdown(
            label="难度等级",
            options=[
                ft.dropdown.Option("简单"),
                ft.dropdown.Option("中等"),
                ft.dropdown.Option("困难"),
                ft.dropdown.Option("专家"),
            ],
            border_radius=10,
        )

        self.status_dropdown = ft.Dropdown(
            label="状态",
            options=[
                ft.dropdown.Option("draft", "草稿"),
                ft.dropdown.Option("published", "已发布"),
                ft.dropdown.Option("archived", "已归档"),
            ],
            value="draft",
            border_radius=10,
        )

        submit_btn = ft.ElevatedButton(
            "💾 保存菜谱",
            icon=ft.icons.SAVE,
            on_click=self.submit_form,
            height=50,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    self.title_field,
                    self.description_field,
                    self.category_dropdown,
                    self.ingredients_area,
                    self.steps_area,
                    ft.Row(
                        controls=[
                            self.cooking_time_field,
                            self.servings_field,
                        ],
                        spacing=20,
                    ),
                    self.difficulty_dropdown,
                    self.status_dropdown,
                    submit_btn,
                ],
                spacing=15,
            ),
            padding=20,
        )

    def did_mount(self):
        """组件挂载后加载数据"""
        # 设置顶部 AppBar
        if self._page:
            title = "编辑菜谱" if self.is_edit else "新建菜谱"
            self._page.appbar = ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: self.on_navigate("/recipes"),
                    icon_color=ft.colors.WHITE,
                ),
                title=ft.Text(title),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
            self._page.update()

        self.load_categories()
        if self.is_edit and self.recipe_id:
            self.load_recipe_data()

    def load_categories(self):
        """加载类别列表"""
        try:
            self.categories = self.category_service.get_all_categories()
            if self.category_dropdown:
                self.category_dropdown.options = [
                    ft.dropdown.Option(cat.name) for cat in self.categories
                ]
                self.update()
        except Exception as e:
            print(f"加载类别失败：{e}")

    def load_recipe_data(self):
        """加载菜谱数据"""
        try:
            self.recipe = self.recipe_service.get_recipe(self.recipe_id)

            if self.recipe and self.title_field:
                self.title_field.value = self.recipe.title
                self.description_field.value = self.recipe.description or ""

                # 设置类别
                if self.recipe.category_id:
                    for cat in self.categories:
                        if cat.id == self.recipe.category_id:
                            self.category_dropdown.value = cat.name
                            break

                # 设置食材（数据库存储的是字符串，直接使用）
                if self.recipe.ingredients:
                    self.ingredients_area.value = self.recipe.ingredients

                # 设置步骤（数据库存储的是字符串，直接使用）
                if self.recipe.steps:
                    self.steps_area.value = self.recipe.steps

                self.cooking_time_field.value = str(self.recipe.cooking_time or "")
                self.servings_field.value = str(self.recipe.servings or "")
                self.difficulty_dropdown.value = self.recipe.difficulty or "简单"
                self.status_dropdown.value = self.recipe.status or "draft"

                self.update()
        except Exception as e:
            print(f"加载菜谱数据失败：{e}")

    def submit_form(self, e):
        """提交表单"""
        # 验证必填字段
        if not self.title_field.value:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ 请输入菜谱名称"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        try:
            # 解析食材和步骤
            ingredients = [item.strip() for item in self.ingredients_area.value.split('\n') if item.strip()]
            steps = [step.strip() for step in self.steps_area.value.split('\n') if step.strip()]

            recipe_data = {
                'title': self.title_field.value,
                'description': self.description_field.value or "",
                'ingredients': ingredients,
                'steps': steps,
                'cooking_time': int(self.cooking_time_field.value) if self.cooking_time_field.value else None,
                'servings': int(self.servings_field.value) if self.servings_field.value else None,
                'difficulty': self.difficulty_dropdown.value or "简单",
                'status': self.status_dropdown.value or "draft",
            }

            if self.is_edit and self.recipe_id:
                success, msg = self.recipe_service.update_recipe(self.recipe_id, recipe_data)
            else:
                success, msg, recipe_id = self.recipe_service.create_recipe(recipe_data)

            if success:
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ 保存成功！"),
                    bgcolor=ft.colors.GREEN,
                )
                self._page.snack_bar.open = True
                self._page.update()

                # 延迟跳转到列表页
                import threading
                threading.Timer(1.0, lambda: self.on_navigate("/recipes")).start()
            else:
                raise Exception(msg)
        except Exception as ex:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 保存失败：{str(ex)}"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()
