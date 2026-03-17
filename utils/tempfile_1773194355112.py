"""
通用对话框工具类
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Dict, Any, List


class CommonDialogs:
    """通用对话框工具类"""

    @staticmethod
   def show_info(message: str, title: str = "提示"):
        """显示信息提示框"""
        messagebox.showinfo(title, message)

    @staticmethod
   def show_error(message: str, title: str = "错误"):
        """显示错误提示框"""
        messagebox.showerror(title, message)

    @staticmethod
   def show_warning(message: str, title: str = "警告"):
        """显示警告提示框"""
        messagebox.showwarning(title, message)

    @staticmethod
   def show_confirm(message: str, title: str = "确认") -> bool:
        """显示确认对话框，返回 True/False"""
        return messagebox.askyesno(title, message)

    @staticmethod
   def ask_question(message: str, title: str = "问题") -> bool:
        """显示是非问答题"""
        return messagebox.askquestion(title, message) == 'yes'


class RecipeDialog(simpledialog.Dialog):
    """菜谱编辑对话框"""

   def __init__(self, parent, title, recipe=None, categories=None):
       self.recipe = recipe
       self.categories = categories or []
       self.result = None
       super().__init__(parent, title)

   def body(self, master):
       ttk.Label(master, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
       self.title_entry = ttk.Entry(master, width=50)
       self.title_entry.grid(row=0, column=1, pady=5)

       ttk.Label(master, text="描述:").grid(row=1, column=0, sticky=tk.W, pady=5)
       self.desc_entry = ttk.Entry(master, width=50)
       self.desc_entry.grid(row=1, column=1, pady=5)

       ttk.Label(master, text="类别:").grid(row=2, column=0, sticky=tk.W, pady=5)
       self.category_var = tk.StringVar()
       self.category_combo = ttk.Combobox(master, textvariable=self.category_var, width=47)
       self.category_combo.grid(row=2, column=1, pady=5)

       category_names = [cat.name for cat in self.categories] if self.categories else []
       self.category_combo['values'] = category_names

       ttk.Label(master, text="难度:").grid(row=3, column=0, sticky=tk.W, pady=5)
       self.difficulty_var = tk.StringVar(value='简单')
        diff_combo = ttk.Combobox(master, textvariable=self.difficulty_var, width=47,
                                  values=['简单', '中等', '困难', '专家'])
        diff_combo.grid(row=3, column=1, pady=5)

       ttk.Label(master, text="烹饪时间 (分钟):").grid(row=4, column=0, sticky=tk.W, pady=5)
       self.time_entry = ttk.Entry(master, width=50)
       self.time_entry.grid(row=4, column=1, pady=5)

       ttk.Label(master, text="份量:").grid(row=5, column=0, sticky=tk.W, pady=5)
       self.servings_entry = ttk.Entry(master, width=50)
       self.servings_entry.grid(row=5, column=1, pady=5)

       ttk.Label(master, text="食材:").grid(row=6, column=0, sticky=tk.W, pady=5)
       self.ingredients_text = tk.Text(master, width=50, height=5)
       self.ingredients_text.grid(row=6, column=1, pady=5)

       ttk.Label(master, text="步骤:").grid(row=7, column=0, sticky=tk.W, pady=5)
       self.steps_text = tk.Text(master, width=50, height=8)
       self.steps_text.grid(row=7, column=1, pady=5)

       ttk.Label(master, text="标签:").grid(row=8, column=0, sticky=tk.W, pady=5)
       self.tags_entry = ttk.Entry(master, width=50)
       self.tags_entry.grid(row=8, column=1, pady=5)

       ttk.Label(master, text="状态:").grid(row=9, column=0, sticky=tk.W, pady=5)
       self.status_var = tk.StringVar(value='draft')
        status_combo = ttk.Combobox(master, textvariable=self.status_var, width=47,
                                    values=['draft-草稿', 'published-已发布'])
        status_combo.grid(row=9, column=1, pady=5)

        if self.recipe:
           self._fill_data()

        return self.title_entry

   def _fill_data(self):
       self.title_entry.insert(0, self.recipe.title)
       self.desc_entry.insert(0, self.recipe.description or '')
        if self.recipe.category_name:
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


class CategoryDialog(simpledialog.Dialog):
    """类别编辑对话框"""

   def __init__(self, parent, title, category=None):
       self.category = category
       self.result = None
       super().__init__(parent, title)

   def body(self, master):
       ttk.Label(master, text="名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
       self.name_entry = ttk.Entry(master, width=40)
       self.name_entry.grid(row=0, column=1, pady=5)

       ttk.Label(master, text="图标:").grid(row=1, column=0, sticky=tk.W, pady=5)
       self.icon_var = tk.StringVar(value='\U0001F37D️')
        icons = ['\U0001F35C', '\U0001F35D', '\U0001F370', '\U0001F964',
                 '\U0001F957', '\U0001F372', '\U0001F354', '\U0001F37D️']
        combo = ttk.Combobox(master, textvariable=self.icon_var, values=icons, width=37)
        combo.grid(row=1, column=1, pady=5)

       ttk.Label(master, text="描述:").grid(row=2, column=0, sticky=tk.W, pady=5)
       self.desc_entry = ttk.Entry(master, width=40)
       self.desc_entry.grid(row=2, column=1, pady=5)

        return self.name_entry

   def apply(self):
       self.result = {
            'name': self.name_entry.get(),
            'icon': self.icon_var.get(),
            'description': self.desc_entry.get()
        }
