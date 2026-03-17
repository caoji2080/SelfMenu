"""
类别管理视图 - 负责菜谱类别的增删改查界面展示
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from models.category_model import Category


class CategoryListView:
    """类别列表视图"""

    def __init__(self, parent, callbacks: dict):
        self.parent = parent
        self.callbacks = callbacks
        self.tree = None

    def create_view(self, parent_frame):
        """创建类别列表视图"""
        # 类别列表
        list_frame = ttk.LabelFrame(parent_frame, text="🏷️ 菜谱类别", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('ID', '图标', '名称', '描述', '排序')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # 设置列宽
        column_widths = {'ID': 50, '图标': 60, '名称': 120, '描述': 200, '排序': 60}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return list_frame

    def load_categories(self, categories: list):
        """加载类别数据"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for category in categories:
            self.tree.insert('', tk.END, values=(
                category.id,
                category.icon,
                category.name,
                category.description,
                category.sort_order
            ))

    def get_selected_category(self) -> Optional[int]:
        """获取选中的类别 ID"""
        selection = self.tree.selection()
        if not selection:
            return None
        item = self.tree.item(selection[0])
        return item['values'][0]


class CategoryDialogView:
    """类别对话框视图"""

    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.widgets = {}

    def create_dialog(self, title: str, category: Optional[Category] = None):
        """创建类别编辑对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # 名称
        ttk.Label(frame, text="名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame, width=40)
        name_entry.grid(row=0, column=1, pady=5)
        self.widgets['name'] = name_entry

        # 图标
        ttk.Label(frame, text="图标:").grid(row=1, column=0, sticky=tk.W, pady=5)
        icon_var = tk.StringVar(value='🍽️')
        icons = ['🍜', '🍝', '🍰', '🥤', '🥗', '🍲', '🍔', '🍽️']
        icon_combo = ttk.Combobox(frame, textvariable=icon_var, values=icons, width=37)
        icon_combo.grid(row=1, column=1, pady=5)
        self.widgets['icon'] = icon_var

        # 描述
        ttk.Label(frame, text="描述:").grid(row=2, column=0, sticky=tk.W, pady=5)
        desc_entry = ttk.Entry(frame, width=40)
        desc_entry.grid(row=2, column=1, pady=5)
        self.widgets['description'] = desc_entry

        # 排序
        ttk.Label(frame, text="排序:").grid(row=3, column=0, sticky=tk.W, pady=5)
        sort_entry = ttk.Entry(frame, width=40)
        sort_entry.grid(row=3, column=1, pady=5)
        self.widgets['sort_order'] = sort_entry

        # 填充现有数据
        if category:
            name_entry.insert(0, category.name)
            icon_var.set(category.icon)
            desc_entry.insert(0, category.description or '')
            sort_entry.insert(0, str(category.sort_order))

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        def on_ok():
            try:
                self.result = {
                    'name': name_entry.get(),
                    'icon': icon_var.get(),
                    'description': desc_entry.get(),
                    'sort_order': int(sort_entry.get()) if sort_entry.get() else 0
                }
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "排序必须是数字")

        ttk.Button(btn_frame, text="确定", command=on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消",
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()
        return self.result
