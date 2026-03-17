"""
菜谱编辑对话框
"""
import tkinter as tk
from tkinter import ttk, simpledialog


class RecipeDialog(simpledialog.Dialog):
    """菜谱编辑对话框"""

    def __init__(self, parent, title, recipe=None, categories=None):
        self.recipe = recipe
        self.categories = categories or []
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        # 标题
        ttk.Label(master, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(master, width=50)
        self.title_entry.grid(row=0, column=1, pady=5)
        self.title_entry.bind('<Return>', lambda e: self.desc_entry.focus_set())

        # 描述
        ttk.Label(master, text="描述:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(master, width=50)
        self.desc_entry.grid(row=1, column=1, pady=5)
        self.desc_entry.bind('<Return>', lambda e: self.category_combo.focus_set())

        # 类别
        ttk.Label(master, text="类别:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(master, textvariable=self.category_var, width=47)
        self.category_combo.grid(row=2, column=1, pady=5)

        if self.categories:
            category_names = [cat.name for cat in self.categories]
            self.category_combo['values'] = category_names

        self.category_combo.bind('<Return>', lambda e: self.difficulty_var_combo.focus_set())

        # 难度
        ttk.Label(master, text="难度:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.difficulty_var = tk.StringVar(value='简单')
        self.difficulty_var_combo = ttk.Combobox(master, textvariable=self.difficulty_var, width=47)
        self.difficulty_var_combo['values'] = ['简单', '中等', '困难', '专家']
        self.difficulty_var_combo.grid(row=3, column=1, pady=5)
        self.difficulty_var_combo.bind('<Return>', lambda e: self.time_entry.focus_set())

        # 烹饪时间
        ttk.Label(master, text="烹饪时间 (分钟):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.time_entry = ttk.Entry(master, width=50)
        self.time_entry.grid(row=4, column=1, pady=5)
        self.time_entry.bind('<Return>', lambda e: self.servings_entry.focus_set())

        # 份量
        ttk.Label(master, text="份量:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.servings_entry = ttk.Entry(master, width=50)
        self.servings_entry.grid(row=5, column=1, pady=5)
        self.servings_entry.bind('<Return>', lambda e: self.ingredients_text.focus_set())

        # 食材
        ttk.Label(master, text="食材:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.ingredients_text = tk.Text(master, width=50, height=5)
        self.ingredients_text.grid(row=6, column=1, pady=5)

        # 步骤
        ttk.Label(master, text="步骤:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.steps_text = tk.Text(master, width=50, height=8)
        self.steps_text.grid(row=7, column=1, pady=5)

        # 标签
        ttk.Label(master, text="标签:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.tags_entry = ttk.Entry(master, width=50)
        self.tags_entry.grid(row=8, column=1, pady=5)
        self.tags_entry.bind('<Return>', lambda e: self.status_combo.focus_set())

        # 状态
        ttk.Label(master, text="状态:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.status_var = tk.StringVar(value='draft')
        self.status_combo = ttk.Combobox(master, textvariable=self.status_var, width=47)
        self.status_combo['values'] = ['draft-草稿', 'published-已发布']
        self.status_combo.grid(row=9, column=1, pady=5)
        self.status_combo.bind('<Return>', lambda e: self.ok_btn.focus_set())

        # 存储按钮引用
        self.ok_btn = None

        if self.recipe:
            self._fill_data()

        return self.title_entry

    def buttonbox(self):
        """自定义按钮，保存 OK 按钮的引用"""
        box = tk.Frame(self)
        w = tk.Button(box, text="确定", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.ok_btn = w

        w = tk.Button(box, text="取消", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        # Deleted:self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def _fill_data(self):
        self.title_entry.insert(0, self.recipe.title)
        self.desc_entry.insert(0, self.recipe.description or '')
        if hasattr(self.recipe, 'category_name') and self.recipe.category_name:
            self.category_var.set(self.recipe.category_name)
        self.difficulty_var.set(self.recipe.difficulty)
        self.time_entry.insert(0, str(self.recipe.cooking_time))
        self.servings_entry.insert(0, str(self.recipe.servings))
        self.ingredients_text.insert('1.0', self.recipe.ingredients)
        self.steps_text.insert('1.0', self.recipe.steps)
        self.tags_entry.insert(0, self.recipe.tags or '')
        self.status_var.set(self.recipe.status)

    def apply(self):
        status = 'published' if 'published' in self.status_var.get() else 'draft'
        self.result = {
            'title': self.title_entry.get(),
            'description': self.desc_entry.get(),
            'category_name': self.category_var.get(),
            'difficulty': self.difficulty_var.get(),
            'cooking_time': int(self.time_entry.get()) if self.time_entry.get() else 0,
            'servings': int(self.servings_entry.get()) if self.servings_entry.get() else 1,
            'ingredients': self.ingredients_text.get('1.0', tk.END).strip(),
            'steps': self.steps_text.get('1.0', tk.END).strip(),
            'tags': self.tags_entry.get(),
            'status': status
        }
