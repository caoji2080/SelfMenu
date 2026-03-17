
"""
菜谱管理视图 - 负责菜谱的增删改查界面展示
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from models.recipe_model import Recipe


class RecipeListView:
    """菜谱列表视图"""

    def __init__(self, parent, callbacks: dict):
        self.parent = parent
        self.callbacks = callbacks  # 包含各种回调函数
        self.tree = None
        self.search_var = None

    def create_view(self, parent_frame):
        """创建菜谱列表视图"""
        # 搜索栏
        search_frame = ttk.Frame(parent_frame)
        search_frame.pack(fill=tk.X, pady=10)

        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(search_frame, text="搜索",
                  command=self.callbacks.get('on_search')).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="清除",
                  command=self.clear_search).pack(side=tk.LEFT, padx=5)

        # 菜谱列表
        list_frame = ttk.LabelFrame(parent_frame, text="📋 菜谱列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('ID', '标题', '类别', '难度', '时间', '状态', '创建时间')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # 设置列宽
        column_widths = {'ID': 50, '标题': 250, '类别': 100,
                        '难度': 80, '时间': 80, '状态': 80, '创建时间': 150}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定双击事件
        self.tree.bind('<Double-1>', lambda e: self.callbacks.get('on_view')())

        return list_frame

    def load_recipes(self, recipes: list):
        """加载菜谱数据到列表"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for recipe in recipes:
            self.tree.insert('', tk.END, values=(
                recipe.id,
                recipe.title,
                recipe.category_name or '未分类',
                recipe.difficulty,
                f'{recipe.cooking_time}分钟',
                recipe.status,
                recipe.created_at
            ))

    def get_selected_recipe(self) -> Optional[int]:
        """获取选中的菜谱 ID"""
        selection = self.tree.selection()
        if not selection:
            return None
        item = self.tree.item(selection[0])
        return item['values'][0]

    def clear_search(self):
        """清除搜索条件"""
        self.search_var.set("")
        if self.callbacks.get('on_clear_search'):
            self.callbacks.get('on_clear_search')()


class RecipeDetailView:
    """菜谱详情视图"""

    def __init__(self, parent):
        self.parent = parent
        self.widgets = {}

    def create_view(self, recipe: Recipe):
        """创建菜谱详情视图"""
        detail_window = tk.Toplevel(self.parent)
        detail_window.title(f"📖 {recipe.title}")
        detail_window.geometry("600x500")

        frame = ttk.Frame(detail_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(frame, text=recipe.title,
                 font=('Arial', 18, 'bold')).pack(anchor=tk.W)

        # 描述
        ttk.Label(frame, text=f"描述：{recipe.description or '无'}").pack(anchor=tk.W, pady=5)

        # 分隔线
        ttk.Separator(frame).pack(fill=tk.X, pady=15)

        # 基本信息
        info_frame = ttk.LabelFrame(frame, text="基本信息", padding=10)
        info_frame.pack(fill=tk.X, pady=10)

        ttk.Label(info_frame, text=f"类别：{recipe.category_name or '未分类'}").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(info_frame, text=f"难度：{recipe.difficulty}").grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(info_frame, text=f"烹饪时间：{recipe.cooking_time}分钟").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(info_frame, text=f"份量：{recipe.servings}人").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(info_frame, text=f"状态：{recipe.status}").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(info_frame, text=f"标签：{recipe.tags or '无'}").grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # 食材
        ingredients_frame = ttk.LabelFrame(frame, text="【食材】", padding=10)
        ingredients_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        ingredients_text = tk.Text(ingredients_frame, height=5, wrap=tk.WORD)
        ingredients_text.pack(fill=tk.BOTH, expand=True)
        ingredients_text.insert('1.0', recipe.ingredients)
        ingredients_text.config(state='disabled')

        # 步骤
        steps_frame = ttk.LabelFrame(frame, text="【步骤】", padding=10)
        steps_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        steps_text = tk.Text(steps_frame, height=10, wrap=tk.WORD)
        steps_text.pack(fill=tk.BOTH, expand=True)
        steps_text.insert('1.0', recipe.steps)
        steps_text.config(state='disabled')

        return detail_window
