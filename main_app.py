"""
主应用控制器 - 整合各模块，控制应用流程
"""
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, Optional
from services.recipe_service import RecipeService
from services.category_service import CategoryService
from views.main_window_view import MainWindowView
from views.recipe_view import RecipeListView, RecipeDetailView
from views.category_view import CategoryListView, CategoryDialogView
from utils.constant_def import RecipeStatus, DifficultyLevel
from utils.event_bus import EventBus, RecipeEvents, CategoryEvents, AppEvents, Event
from utils.dialogs import RecipeDialog, CategoryDialog, CommonDialogs
from models.recipe_model import Recipe
from models.category_model import Category


class MainApplication:
    """主应用控制器"""

    def __init__(self, root, recipe_service: RecipeService, category_service: CategoryService):
        self.root = root
        self.recipe_service = recipe_service
        self.category_service = category_service
        self.event_bus = EventBus()
        self.current_page = 1
        self.page_size = 10
        self._setup_ui()
        self._register_event_listeners()
        self._load_initial_data()
        self.event_bus.publish(Event(AppEvents.APP_STARTED))

    def _setup_ui(self):
        """设置 UI"""
        callbacks = {
            'on_new_recipe': self.add_recipe,
            'on_manage_categories': self.manage_categories,
            'on_search': self.open_search,
            'on_import_export': self.open_import_export,
            'on_refresh': self.refresh_all,
            'on_prev_page': self.prev_page,
            'on_next_page': self.next_page
        }
        self.main_view = MainWindowView(self.root, callbacks)
        self.main_view.create_main_layout()

        recipe_callbacks = {
            'on_view': self.view_recipe,
            'on_edit': self.edit_recipe,
            'on_delete': self.delete_recipe,
            'on_search': self.do_search,
            'on_clear_search': self.clear_search
        }
        self.recipe_list_view = RecipeListView(
            self.main_view.get_content_frame(),
            recipe_callbacks
        )
        self.recipe_list_view.create_view(self.main_view.get_content_frame())

    def _register_event_listeners(self):
        """注册事件监听"""
        self.event_bus.subscribe(RecipeEvents.RECIPE_CREATED, lambda e: self._on_recipe_changed())
        self.event_bus.subscribe(RecipeEvents.RECIPE_UPDATED, lambda e: self._on_recipe_changed())
        self.event_bus.subscribe(RecipeEvents.RECIPE_DELETED, lambda e: self._on_recipe_changed())
        self.event_bus.subscribe(CategoryEvents.CATEGORY_CREATED, lambda e: self._on_category_changed())
        self.event_bus.subscribe(CategoryEvents.CATEGORY_UPDATED, lambda e: self._on_category_changed())
        self.event_bus.subscribe(CategoryEvents.CATEGORY_DELETED, lambda e: self._on_category_changed())

    def _on_recipe_changed(self):
        """菜谱变化时的处理"""
        self.refresh_all()

    def _on_category_changed(self):
        """类别变化时的处理"""
        self.refresh_all()

    def _load_initial_data(self):
        """加载初始数据"""
        self.refresh_all()

    def refresh_all(self):
        """刷新所有数据"""
        all_recipes = self.recipe_service.get_all_recipes()
        all_categories = self.category_service.get_all_categories()
        stats = {
            'recipes': len(all_recipes),
            'categories': len(all_categories),
            'published': len([r for r in all_recipes if r.status == 'published'])
        }
        self.main_view.update_stats(stats)
        self.load_recipes()
        self.event_bus.publish(Event(AppEvents.DATA_REFRESHED))

    def load_recipes(self):
        """加载菜谱列表"""
        recipes = self.recipe_service.get_all_recipes(page=self.current_page, page_size=self.page_size)
        self.recipe_list_view.load_recipes(recipes)
        self.main_view.update_page_info(self.current_page)

    def add_recipe(self):
        """添加菜谱"""
        categories = self.category_service.get_all_categories()
        dialog = RecipeDialog(self.root, "新建菜谱", categories=categories)

        if dialog.result:
            try:
                recipe_data = dialog.result
                category_id = None
                if recipe_data.get('category_name'):
                    for cat in categories:
                        if cat.name == recipe_data['category_name']:
                            category_id = cat.id
                            break

                recipe = Recipe(
                    title=recipe_data['title'],
                    description=recipe_data['description'],
                    category_id=category_id,
                    ingredients=recipe_data['ingredients'],
                    steps=recipe_data['steps'],
                    cooking_time=recipe_data['cooking_time'],
                    difficulty=recipe_data['difficulty'],
                    servings=recipe_data['servings'],
                    tags=recipe_data['tags'],
                    status=recipe_data['status']
                )

                success, msg, recipe_id = self.recipe_service.create_recipe(recipe.to_dict())
                if success:
                    CommonDialogs.show_info("✅ 菜谱创建成功！", "成功")
                    self.event_bus.publish(Event(RecipeEvents.RECIPE_CREATED))
                else:
                    CommonDialogs.show_error(f"创建失败：{msg}", "错误")
            except Exception as e:
                CommonDialogs.show_error(f"创建失败：{str(e)}", "错误")

    def edit_recipe(self):
        """编辑菜谱"""
        recipe_id = self.recipe_list_view.get_selected_recipe()
        if not recipe_id:
            CommonDialogs.show_warning("请先选择要编辑的菜谱", "提示")
            return

        recipe = self.recipe_service.get_recipe(recipe_id)
        if recipe:
            categories = self.category_service.get_all_categories()
            dialog = RecipeDialog(self.root, "编辑菜谱", recipe=recipe, categories=categories)

            if dialog.result:
                try:
                    recipe_data = dialog.result
                    category_id = None
                    if recipe_data.get('category_name'):
                        for cat in categories:
                            if cat.name == recipe_data['category_name']:
                                category_id = cat.id
                                break

                    updated_recipe = Recipe(
                        id=recipe_id,
                        title=recipe_data['title'],
                        description=recipe_data['description'],
                        category_id=category_id,
                        ingredients=recipe_data['ingredients'],
                        steps=recipe_data['steps'],
                        cooking_time=recipe_data['cooking_time'],
                        difficulty=recipe_data['difficulty'],
                        servings=recipe_data['servings'],
                        tags=recipe_data['tags'],
                        status=recipe_data['status']
                    )

                    success, msg = self.recipe_service.update_recipe(recipe_id, updated_recipe.to_dict())
                    if success:
                        CommonDialogs.show_info("✅ 菜谱已更新！", "成功")
                        self.event_bus.publish(Event(RecipeEvents.RECIPE_UPDATED))
                    else:
                        CommonDialogs.show_error(f"更新失败：{msg}", "错误")
                except Exception as e:
                    CommonDialogs.show_error(f"更新失败：{str(e)}", "错误")

    def delete_recipe(self):
        """删除菜谱"""
        recipe_id = self.recipe_list_view.get_selected_recipe()
        if not recipe_id:
            CommonDialogs.show_warning("请先选择要删除的菜谱", "提示")
            return

        if CommonDialogs.show_confirm("确定要删除这个菜谱吗？", "确认"):
            try:
                success, msg = self.recipe_service.delete_recipe(recipe_id)
                if success:
                    CommonDialogs.show_info("✅ 菜谱已删除", "成功")
                    self.event_bus.publish(Event(RecipeEvents.RECIPE_DELETED))
                else:
                    CommonDialogs.show_error(f"删除失败：{msg}", "错误")
            except Exception as e:
                CommonDialogs.show_error(f"删除失败：{str(e)}", "错误")

    def view_recipe(self):
        """查看菜谱详情"""
        recipe_id = self.recipe_list_view.get_selected_recipe()
        if not recipe_id:
            CommonDialogs.show_warning("请先选择要查看的菜谱", "提示")
            return

        recipe = self.recipe_service.get_recipe(recipe_id)
        if recipe:
            detail_view = RecipeDetailView(self.root)
            detail_view.create_view(recipe)
            self.event_bus.publish(Event(RecipeEvents.RECIPE_VIEWED, {'recipe_id': recipe_id}))

    def manage_categories(self):
        """管理类别"""
        win = tk.Toplevel(self.root)
        win.title("🏷️ 类别管理")
        win.geometry("700x500")

        frame = ttk.Frame(win, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        cat_list_view = CategoryListView(win, {})
        cat_list_view.create_view(frame)

        def load_categories():
            categories = self.category_service.get_all_categories()
            cat_list_view.load_categories(categories)

        def add_category():
            dialog_view = CategoryDialogView(win)
            result = dialog_view.create_dialog("添加类别")

            if result:
                try:
                    category = Category(
                        name=result['name'],
                        icon=result['icon'],
                        description=result['description'],
                        sort_order=result.get('sort_order', 0)
                    )
                    success, msg, cat_id = self.category_service.create_category(category.to_dict())
                    if success:
                        load_categories()
                        self.event_bus.publish(Event(CategoryEvents.CATEGORY_CREATED))
                    else:
                        CommonDialogs.show_error(f"添加失败：{msg}", "错误")
                except Exception as e:
                    CommonDialogs.show_error(f"添加失败：{str(e)}", "错误")

        def delete_category():
            cat_id = cat_list_view.get_selected_category()
            if not cat_id:
                return

            if CommonDialogs.show_confirm("确定删除？", "确认"):
                try:
                    success, msg = self.category_service.delete_category(cat_id)
                    if success:
                        load_categories()
                        self.event_bus.publish(Event(CategoryEvents.CATEGORY_DELETED))
                    else:
                        CommonDialogs.show_error(f"删除失败：{msg}", "错误")
                except Exception as e:
                    CommonDialogs.show_error(f"删除失败：{str(e)}", "错误")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ 添加", command=add_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ 删除", command=delete_category).pack(side=tk.LEFT, padx=5)

        load_categories()

    def open_search(self):
        """打开搜索窗口"""
        from views.search_view import SearchView

        search_view = SearchView(self.root, {
            'on_advanced_search': self.advanced_search,
            'load_categories': self.category_service.get_all_categories
        })
        search_view.create_advanced_search()

    def advanced_search(self, criteria: dict):
        """高级搜索"""
        results = self.recipe_service.search_advanced(criteria)
        return results

    def do_search(self):
        """执行搜索"""
        pass

    def clear_search(self):
        """清除搜索"""
        self.load_recipes()

    def open_import_export(self):
        """打开导入导出窗口"""
        from views.import_export_view import ImportExportView

        view = ImportExportView(self.root, {
            'on_export': self.export_recipes,
            'on_import': self.import_recipes
        })
        view.create_import_export_dialog()

    def export_recipes(self, filepath: str, options: dict) -> int:
        """导出菜谱"""
        try:
            from utils.file_utils import ExportManager
            exporter = ExportManager()
            count = exporter.export_recipes(filepath, options)
            return count
        except Exception as e:
            CommonDialogs.show_error(f"导出失败：{str(e)}", "错误")
            return 0

    def import_recipes(self, filepath: str, options: dict) -> dict:
        """导入菜谱"""
        try:
            from utils.file_utils import ImportManager
            importer = ImportManager()
            result = importer.import_recipes(filepath, options)
            self.refresh_all()
            return result
        except Exception as e:
            CommonDialogs.show_error(f"导入失败：{str(e)}", "错误")
            return {'success': 0, 'failed': 0}

    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_recipes()

    def next_page(self):
        """下一页"""
        self.current_page += 1
        self.load_recipes()

    def on_closing(self):
        """关闭窗口时的处理"""
        if CommonDialogs.show_confirm("确定要退出吗？", "退出"):
            self.event_bus.publish(Event(AppEvents.APP_CLOSING))
            self.root.destroy()


def create_application():
    """创建并启动应用"""
    root = tk.Tk()
    root.title("🍳 个人菜谱管理系统")
    root.geometry("1200x800")

    # 执行数据库迁移
    from utils.database import db
    db.init_tables()

    from utils.database_migrator import DatabaseMigrator
    migrator = DatabaseMigrator()
    migrator.migrate()

    recipe_service = RecipeService()
    category_service = CategoryService()

    app = MainApplication(root, recipe_service, category_service)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    print("✅ 应用程序启动成功！")
    print("💡 提示：首次使用建议先添加默认类别\n")

    root.mainloop()

    recipe_service = RecipeService()
    category_service = CategoryService()

    app = MainApplication(root, recipe_service, category_service)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    print("✅ 应用程序启动成功！")
    print("💡 提示：首次使用建议先添加默认类别\n")

    root.mainloop()


if __name__ == "__main__":
    create_application()
