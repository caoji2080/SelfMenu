"""
类别编辑对话框
"""
import tkinter as tk
from tkinter import ttk, simpledialog


class CategoryDialog(simpledialog.Dialog):
  """
  类别编辑对话框
    """


  def __init__(self, parent, title, category=None):
      self.category = category
      self.result = None
      super().__init__(parent, title)


  def body(self, master):

  #名称
    ttk.Label(master, text="名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
    self.name_entry = ttk.Entry(master, width=40)
    self.name_entry.grid(row=0, column=1, pady=5)

      # 图标
    ttk.Label(master, text="图标:").grid(row=1, column=0, sticky=tk.W, pady=5)
    self.icon_var = tk.StringVar()
    icons = ['🍜', '🍝', '🍰', '🥤', '🥗', '🍲', '🍔', '🍽️']
    combo = ttk.Combobox(master, textvariable=self.icon_var, values=icons, width=37)
    combo.grid(row=1, column=1, pady=5)

     # 描述
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