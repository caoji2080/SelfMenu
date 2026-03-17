"""
主窗口视图 - 应用的主界面框架
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict


class MainWindowView:
    """主窗口视图"""

    def __init__(self, root, callbacks: Dict[str, Callable]):
        self.root = root
        self.callbacks = callbacks
        self.main_frame = None
        self.stats_labels = {}
        self.quick_buttons = {}

    def create_main_layout(self):
        """创建主布局"""
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建标题
        self._create_title()

        # 创建统计卡片
        self._create_stats_cards()

        # 创建快速操作区
        self._create_quick_actions()

        # 创建内容区域（用于放置不同的视图）
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建状态栏
        self._create_status_bar()

        return self.main_frame

    def _create_title(self):
        """创建标题"""
        title_lbl = ttk.Label(self.main_frame,
                             text="🎉 个人菜谱管理系统",
                             font=('Arial', 28, 'bold'),
                             foreground='#2196F3')
        title_lbl.pack(pady=(0, 10))

    def _create_stats_cards(self):
        """创建统计卡片"""
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(fill=tk.X, pady=20)

        # 总菜谱数
        card1 = ttk.LabelFrame(stats_frame, text="📖 总菜谱数", padding=25)
        card1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        lbl_recipes = ttk.Label(card1, text="0",
                               font=('Arial', 42, 'bold'),
                               foreground='#2196F3')
        lbl_recipes.pack()
        self.stats_labels['recipes'] = lbl_recipes

        # 类别数
        card2 = ttk.LabelFrame(stats_frame, text="🏷️ 类别数", padding=25)
        card2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        lbl_categories = ttk.Label(card2, text="0",
                                  font=('Arial', 42, 'bold'),
                                  foreground='#4CAF50')
        lbl_categories.pack()
        self.stats_labels['categories'] = lbl_categories

        # 已发布
        card3 = ttk.LabelFrame(stats_frame, text="✅ 已发布", padding=25)
        card3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        lbl_published = ttk.Label(card3, text="0",
                                 font=('Arial', 42, 'bold'),
                                 foreground='#FF9800')
        lbl_published.pack()
        self.stats_labels['published'] = lbl_published

    def _create_quick_actions(self):
        """创建快速操作区"""
        quick_frame = ttk.LabelFrame(self.main_frame, text="⚡ 快速操作", padding=15)
        quick_frame.pack(fill=tk.X, pady=15)

        btn_frame = ttk.Frame(quick_frame)
        btn_frame.pack()

        # 新建菜谱
        btn_new = ttk.Button(btn_frame, text="➕ 新建菜谱",
                            command=self.callbacks.get('on_new_recipe'))
        btn_new.grid(row=0, column=0, padx=8, pady=5)
        self.quick_buttons['new_recipe'] = btn_new

        # 管理类别
        btn_cat = ttk.Button(btn_frame, text="🏷️ 管理类别",
                            command=self.callbacks.get('on_manage_categories'))
        btn_cat.grid(row=0, column=1, padx=8, pady=5)
        self.quick_buttons['manage_categories'] = btn_cat

        # 搜索菜谱
        btn_search = ttk.Button(btn_frame, text="🔍 搜索菜谱",
                               command=self.callbacks.get('on_search'))
        btn_search.grid(row=0, column=2, padx=8, pady=5)
        self.quick_buttons['search'] = btn_search

        # 导入导出
        btn_import = ttk.Button(btn_frame, text="📥 导入导出",
                               command=self.callbacks.get('on_import_export'))
        btn_import.grid(row=0, column=3, padx=8, pady=5)
        self.quick_buttons['import_export'] = btn_import

        # 刷新
        btn_refresh = ttk.Button(btn_frame, text="🔄 刷新",
                                command=self.callbacks.get('on_refresh'))
        btn_refresh.grid(row=0, column=4, padx=8, pady=5)
        self.quick_buttons['refresh'] = btn_refresh

    def _create_status_bar(self):
        """创建状态栏"""
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # 分页信息
        self.page_label = ttk.Label(status_frame, text="第 1 页")
        self.page_label.pack(side=tk.RIGHT, padx=10)

        ttk.Button(status_frame, text="⬅️ 上一页",
                  command=self.callbacks.get('on_prev_page')).pack(side=tk.RIGHT)
        ttk.Button(status_frame, text="下一页 ➡️",
                  command=self.callbacks.get('on_next_page')).pack(side=tk.RIGHT)

        # 统计信息
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)

    def update_stats(self, stats: dict):
        """更新统计信息"""
        if 'recipes' in stats:
            self.stats_labels['recipes'].config(text=str(stats['recipes']))
        if 'categories' in stats:
            self.stats_labels['categories'].config(text=str(stats['categories']))
        if 'published' in stats:
            self.stats_labels['published'].config(text=str(stats['published']))

    def update_page_info(self, page: int):
        """更新页面信息"""
        self.page_label.config(text=f"第 {page} 页")

    def set_status(self, message: str):
        """设置状态栏消息"""
        self.status_label.config(text=message)

    def get_content_frame(self):
        """获取内容区域框架"""
        return self.content_frame
