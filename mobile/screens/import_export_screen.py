# 文件名：mobile/screens/import_export_screen.py
# 目录：mobile/screens/import_export_screen.py
# 功能：导入导出屏幕 - 菜谱数据的导入和导出功能

import flet as ft
from datetime import datetime
from utils.file_utils import FileUtils


class ImportExportScreen(ft.Container):
    """导入导出屏幕"""

    def __init__(self, page: ft.Page, on_navigate, recipe_service):
        super().__init__()
        self._page = page
        self.on_navigate = on_navigate
        self.recipe_service = recipe_service
        self.expand = True

        self.content = self._build_screen()

    def _build_screen(self):
        """构建导入导出界面"""
        return ft.Column(
            controls=[
                self._create_export_section(),
                self._create_import_section(),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _create_export_section(self):
        """创建导出区域"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("📤 导出数据", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("选择要导出的菜谱范围："),
                    ft.RadioGroup(
                        content=ft.Column(
                            controls=[
                                ft.Radio(value="all", label="全部菜谱"),
                                ft.Radio(value="recent", label="最近更新的菜谱"),
                                ft.Radio(value="selected", label="手动选择"),
                            ]
                        ),
                        value="all",
                    ),
                    ft.ElevatedButton(
                        "导出为 JSON",
                        icon=ft.icons.FILE_DOWNLOAD,
                        on_click=self.export_json,
                    ),
                    ft.ElevatedButton(
                        "导出为 CSV",
                        icon=ft.icons.FILE_DOWNLOAD,
                        on_click=self.export_csv,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _create_import_section(self):
        """创建导入区域"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("📥 导入数据", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("选择要导入的文件格式："),
                    ft.RadioGroup(
                        content=ft.Column(
                            controls=[
                                ft.Radio(value="json", label="JSON 格式"),
                                ft.Radio(value="csv", label="CSV 格式"),
                            ]
                        ),
                        value="json",
                    ),
                    ft.ElevatedButton(
                        "选择文件",
                        icon=ft.icons.FOLDER_OPEN,
                        on_click=self.import_file,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
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
                title=ft.Text("导入导出"),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
            )
            self._page.update()

    def export_json(self, e):
        """导出为 JSON"""
        try:
            # 获取所有菜谱数据
            print("📤 开始导出 JSON...")
            all_recipes = self.recipe_service.get_all_recipes()

            if not all_recipes:
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("⚠️ 暂无菜谱可导出"),
                    bgcolor=ft.colors.ORANGE,
                )
                self._page.snack_bar.open = True
                self._page.update()
                return

            # 转换为字典列表
            recipes_data = [recipe.to_dict() for recipe in all_recipes]

            # 生成文件名（带时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recipes_export_{timestamp}.json"

            print(f"💾 导出 {len(recipes_data)} 条记录到 {filename}")

            # 使用 FileUtils 导出
            success = FileUtils.export_to_json(recipes_data, filename)

            if success:
                print(f"✅ 导出成功：{filename}")
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"✅ 导出成功！\n已导出 {len(recipes_data)} 条菜谱\n文件：{filename}"),
                    bgcolor=ft.colors.GREEN,
                    duration=3000,
                )
                self._page.snack_bar.open = True
                self._page.update()
            else:
                raise Exception("导出失败")

        except Exception as ex:
            print(f"❌ 导出异常：{ex}")
            import traceback
            traceback.print_exc()
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 导出失败：{str(ex)}"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()

    def export_csv(self, e):
        """导出为 CSV"""
        try:
            # 获取所有菜谱数据
            print("📤 开始导出 CSV...")
            all_recipes = self.recipe_service.get_all_recipes()

            if not all_recipes:
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text("⚠️ 暂无菜谱可导出"),
                    bgcolor=ft.colors.ORANGE,
                )
                self._page.snack_bar.open = True
                self._page.update()
                return

            # 转换为字典列表，并过滤掉不需要的字段
            recipes_data = []
            for recipe in all_recipes:
                recipe_dict = recipe.to_dict()
                # 只保留 CSV 需要的字段
                filtered_dict = {
                    'id': recipe_dict.get('id'),
                    'title': recipe_dict.get('title'),
                    'description': recipe_dict.get('description'),
                    'category_id': recipe_dict.get('category_id'),
                    'category_name': recipe_dict.get('category_name', ''),
                    'ingredients': recipe_dict.get('ingredients'),
                    'steps': recipe_dict.get('steps'),
                    'cooking_time': recipe_dict.get('cooking_time'),
                    'difficulty': recipe_dict.get('difficulty'),
                    'servings': recipe_dict.get('servings'),
                    'status': recipe_dict.get('status'),
                    'tags': recipe_dict.get('tags'),
                    'rating': recipe_dict.get('rating'),
                    'view_count': recipe_dict.get('view_count'),
                }
                recipes_data.append(filtered_dict)

            # 定义 CSV 字段
            fieldnames = [
                'id', 'title', 'description', 'category_id', 'category_name',
                'ingredients', 'steps', 'cooking_time', 'difficulty',
                'servings', 'status', 'tags', 'rating', 'view_count'
            ]

            # 生成文件名（带时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recipes_export_{timestamp}.csv"

            print(f"💾 导出 {len(recipes_data)} 条记录到 {filename}")

            # 使用 FileUtils 导出
            success = FileUtils.export_to_csv(recipes_data, filename, fieldnames)

            if success:
                print(f"✅ 导出成功：{filename}")
                self._page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"✅ 导出成功！\n已导出 {len(recipes_data)} 条菜谱\n文件：{filename}"),
                    bgcolor=ft.colors.GREEN,
                    duration=3000,
                )
                self._page.snack_bar.open = True
                self._page.update()
            else:
                raise Exception("导出失败")

        except Exception as ex:
            print(f"❌ 导出异常：{ex}")
            import traceback
            traceback.print_exc()
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 导出失败：{str(ex)}"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()

    def import_file(self, e):
        """导入文件"""
        try:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text("此功能开发中..."),
                bgcolor=ft.colors.ORANGE,
            )
            self._page.snack_bar.open = True
            self._page.update()
        except Exception as ex:
            self._page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ 导入失败：{str(ex)}"),
                bgcolor=ft.colors.RED,
            )
            self._page.snack_bar.open = True
            self._page.update()
