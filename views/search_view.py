
"""
搜索视图 - 负责菜谱搜索功能的界面展示
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class SearchView:
    """搜索视图"""

    def __init__(self, parent, callbacks: dict):
        self.parent = parent
        self.callbacks = callbacks
        self.advanced_window = None

    def create_advanced_search(self):
        """创建高级搜索窗口"""
        self.advanced_window = tk.Toplevel(self.parent)
        self.advanced_window.title("🔍 高级搜索")
        self.advanced_window.geometry("600x500")

        frame = ttk.Frame(self.advanced_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # 关键词搜索
        search_frame = ttk.LabelFrame(frame, text="关键词搜索", padding=10)
        search_frame.pack(fill=tk.X, pady=10)

        ttk.Label(search_frame, text="标题/描述:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.keyword_entry = ttk.Entry(search_frame, width=50)
        self.keyword_entry.grid(row=0, column=1, pady=5)

        # 条件筛选
        filter_frame = ttk.LabelFrame(frame, text="筛选条件", padding=10)
        filter_frame.pack(fill=tk.X, pady=10)

        # 类别筛选
        ttk.Label(filter_frame, text="类别:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, width=47)
        category_combo.grid(row=0, column=1, pady=5)

        # 难度筛选
        ttk.Label(filter_frame, text="难度:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.difficulty_var = tk.StringVar()
        difficulty_combo = ttk.Combobox(filter_frame, textvariable=self.difficulty_var,
                                       values=['全部', '简单', '中等', '困难', '专家'], width=47)
        difficulty_combo.grid(row=1, column=1, pady=5)
        difficulty_combo.set('全部')

        # 时间范围
        ttk.Label(filter_frame, text="烹饪时间:").grid(row=2, column=0, sticky=tk.W, pady=5)
        time_frame = ttk.Frame(filter_frame)
        time_frame.grid(row=2, column=1, pady=5, sticky=tk.W)

        self.time_min_entry = ttk.Entry(time_frame, width=10)
        self.time_min_entry.pack(side=tk.LEFT)
        ttk.Label(time_frame, text=" - ").pack(side=tk.LEFT)
        self.time_max_entry = ttk.Entry(time_frame, width=10)
        self.time_max_entry.pack(side=tk.LEFT)
        ttk.Label(time_frame, text=" 分钟").pack(side=tk.LEFT)

        # 标签筛选
        ttk.Label(filter_frame, text="标签:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.tags_entry = ttk.Entry(filter_frame, width=47)
        self.tags_entry.grid(row=3, column=1, pady=5)

        # 搜索结果
        result_frame = ttk.LabelFrame(frame, text="搜索结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('ID', '标题', '类别', '难度', '时间')
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.result_tree.heading(col, text=col)
            w = 60 if col == 'ID' else 150
            self.result_tree.column(col, width=w)

        self.result_tree.pack(fill=tk.BOTH, expand=True)

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="搜索",
                  command=self._do_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="重置",
                  command=self._reset_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="关闭",
                  command=self.advanced_window.destroy).pack(side=tk.RIGHT, padx=5)

        # 加载类别列表
        if self.callbacks.get('load_categories'):
            categories = self.callbacks.get('load_categories')()
            category_names = [cat.name for cat in categories] if categories else []
            category_combo['values'] = ['全部'] + category_names
            self.category_var.set('全部')

        return self.advanced_window

    def _do_search(self):
        """执行搜索"""
        if self.callbacks.get('on_advanced_search'):
            criteria = {
                'keyword': self.keyword_entry.get(),
                'category': self.category_var.get() if self.category_var.get() != '全部' else None,
                'difficulty': self.difficulty_var.get() if self.difficulty_var.get() != '全部' else None,
                'time_min': int(self.time_min_entry.get()) if self.time_min_entry.get() else None,
                'time_max': int(self.time_max_entry.get()) if self.time_max_entry.get() else None,
                'tags': self.tags_entry.get()
            }
            results = self.callbacks.get('on_advanced_search')(criteria)
            self._display_results(results)

    def _reset_search(self):
        """重置搜索条件"""
        self.keyword_entry.delete(0, tk.END)
        self.category_var.set('全部')
        self.difficulty_var.set('全部')
        self.time_min_entry.delete(0, tk.END)
        self.time_max_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)

        # 清空结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def _display_results(self, results: list):
        """显示搜索结果"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        for recipe in results:
            self.result_tree.insert('', tk.END, values=(
                recipe.id,
                recipe.title,
                recipe.category_name or '未分类',
                recipe.difficulty,
                f'{recipe.cooking_time}分钟'
            ))
