"""
建立模块化的个人菜谱APP应用，主要包含创建菜谱（增删改查）模块、菜谱类别管理（增删改查）模块、
菜谱分类展示模块、菜谱分享管理模块、菜谱导入导出模块、菜谱搜索查询模块等六个模块。

"""
"""
个人菜谱管理系统 - 技术原型 v1.0
完整可运行版本
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from pathlib import Path
from datetime import datetime

# ==================== 配置 ====================
APP_NAME = "🍳 个人菜谱管理系统"
VERSION = "v1.0 技术原型"
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "menu_app.db"

# ==================== 数据库层 ====================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.init_tables()

    def init_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                icon TEXT DEFAULT '🍽️',
                sort_order INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category_id INTEGER,
                ingredients TEXT,
                steps TEXT,
                cooking_time INTEGER DEFAULT 0,
                difficulty TEXT DEFAULT '简单',
                servings INTEGER DEFAULT 1,
                status TEXT DEFAULT 'draft',
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def execute(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor

    def fetchone(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetchall(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

# ==================== 对话框类 ====================
class RecipeDialog(simpledialog.Dialog):
    def __init__(self, parent, title, recipe=None):
        self.recipe = recipe
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
        self.title_entry.insert(0, self.recipe['title'])
        self.desc_entry.insert(0, self.recipe['description'] or '')
        if self.recipe.get('category_name'):
            self.category_var.set(self.recipe['category_name'])
        self.difficulty_var.set(self.recipe['difficulty'])
        self.time_entry.insert(0, str(self.recipe['cooking_time']))
        self.servings_entry.insert(0, str(self.recipe['servings']))
        self.ingredients_text.insert('1.0', self.recipe['ingredients'])
        self.steps_text.insert('1.0', self.recipe['steps'])
        self.tags_entry.insert(0, self.recipe['tags'] or '')
        self.status_var.set(self.recipe['status'])

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
    def __init__(self, parent, title):
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(master, width=40)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(master, text="图标:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.icon_var = tk.StringVar(value='🍽️')
        icons = ['🍜', '🍝', '🍰', '🥤', '🥗', '🍲', '🍔', '🍽️']
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

# ==================== 主应用类 ====================
class MenuApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} {VERSION}")
        self.root.geometry("1200x800")

        self.db = Database()
        self.page = 1
        self.page_size = 15

        self.create_ui()
        self.refresh_all()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_ui(self):
        main = ttk.Frame(self.root, padding="20")
        main.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_lbl = ttk.Label(main, text=f"🎉 {APP_NAME}",
                             font=('Arial', 28, 'bold'), foreground='#2196F3')
        title_lbl.pack(pady=(0, 10))

        # 统计卡片
        stats = ttk.Frame(main)
        stats.pack(fill=tk.X, pady=20)

        card1 = ttk.LabelFrame(stats, text="📖 总菜谱数", padding=25)
        card1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.lbl_recipes = ttk.Label(card1, text="0", font=('Arial', 42, 'bold'), foreground='#2196F3')
        self.lbl_recipes.pack()

        card2 = ttk.LabelFrame(stats, text="🏷️ 类别数", padding=25)
        card2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.lbl_categories = ttk.Label(card2, text="0", font=('Arial', 42, 'bold'), foreground='#4CAF50')
        self.lbl_categories.pack()

        # 快速操作
        quick = ttk.LabelFrame(main, text="⚡ 快速操作", padding=15)
        quick.pack(fill=tk.X, pady=15)

        qbtn = ttk.Frame(quick)
        qbtn.pack()

        ttk.Button(qbtn, text="➕ 新建菜谱", command=self.add_recipe).grid(row=0, column=0, padx=8, pady=5)
        ttk.Button(qbtn, text="🏷️ 管理类别", command=self.manage_categories).grid(row=0, column=1, padx=8, pady=5)
        ttk.Button(qbtn, text="🔍 搜索菜谱", command=self.search).grid(row=0, column=2, padx=8, pady=5)
        ttk.Button(qbtn, text="📊 刷新", command=self.refresh_all).grid(row=0, column=3, padx=8, pady=5)
        ttk.Button(qbtn, text="🏷️ 默认类别", command=self.add_defaults).grid(row=0, column=4, padx=8, pady=5)

        # 搜索栏
        search_f = ttk.Frame(main)
        search_f.pack(fill=tk.X, pady=(10, 0))

        self.search_var = tk.StringVar()
        ttk.Entry(search_f, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(search_f, text="搜索", command=self.do_search).pack(side=tk.LEFT)
        ttk.Button(search_f, text="清除", command=self.clear_search).pack(side=tk.LEFT, padx=5)

        # 菜谱列表
        list_f = ttk.LabelFrame(main, text="📋 菜谱列表", padding=10)
        list_f.pack(fill=tk.BOTH, expand=True, pady=15)

        cols = ('ID', '标题', '类别', '难度', '时间', '状态')
        self.tree = ttk.Treeview(list_f, columns=cols, show='headings', height=15)

        for col in cols:
            w = 60 if col in ['ID', '难度'] else 120
            if col == '标题': w = 350
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w)

        sb = ttk.Scrollbar(list_f, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Double-1>', lambda e: self.view_recipe())

        # 底部按钮
        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X, pady=(10, 0))

        b1 = ttk.Frame(bottom)
        b1.pack(side=tk.LEFT)
        ttk.Button(b1, text="👁️ 查看", command=self.view_recipe).pack(side=tk.LEFT, padx=5)
        ttk.Button(b1, text="✏️ 编辑", command=self.edit_recipe).pack(side=tk.LEFT, padx=5)
        ttk.Button(b1, text="🗑️ 删除", command=self.delete_recipe).pack(side=tk.LEFT, padx=5)

        b2 = ttk.Frame(bottom)
        b2.pack(side=tk.RIGHT)
        ttk.Button(b2, text="⬅️ 上一页", command=self.prev_page).pack(side=tk.LEFT)
        self.lbl_page = ttk.Label(b2, text="第 1 页")
        self.lbl_page.pack(side=tk.LEFT, padx=10)
        ttk.Button(b2, text="下一页 ➡️", command=self.next_page).pack(side=tk.LEFT)

    def refresh_all(self):
        recipes = self.db.fetchall("SELECT COUNT(*) as cnt FROM recipes")
        cats = self.db.fetchall("SELECT COUNT(*) as cnt FROM categories")
        self.lbl_recipes.config(text=str(recipes[0]['cnt'] if recipes else 0))
        self.lbl_categories.config(text=str(cats[0]['cnt'] if cats else 0))
        self.load_recipes()

    def load_recipes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        offset = (self.page - 1) * self.page_size
        sql = """
            SELECT r.id, r.title, c.name as category_name, r.difficulty, 
                   r.cooking_time, r.status
            FROM recipes r LEFT JOIN categories c ON r.category_id = c.id
            ORDER BY r.created_at DESC LIMIT ? OFFSET ?
        """
        recipes = self.db.fetchall(sql, (self.page_size, offset))

        icons = {'简单': '⭐', '中等': '⭐⭐', '困难': '⭐⭐⭐', '专家': '⭐⭐⭐⭐'}
        for r in recipes:
            t = f"{r['cooking_time']}分钟" if r['cooking_time'] < 60 else f"{r['cooking_time']//60}h{r['cooking_time']%60}m"
            s = '✅' if r['status'] == 'published' else '📝'
            self.tree.insert('', tk.END, values=(
                r['id'], r['title'], r['category_name'] or '未分类',
                icons.get(r['difficulty'], '⭐'), t, s
            ))
        self.lbl_page.config(text=f"第 {self.page} 页")

    def add_recipe(self):
        d = RecipeDialog(self.root, "新建菜谱")
        if d.result:
            cat_id = None
            if d.result['category_name']:
                c = self.db.fetchone("SELECT id FROM categories WHERE name=?", (d.result['category_name'],))
                cat_id = c['id'] if c else None

            self.db.execute("""
                INSERT INTO recipes (title, description, category_id, ingredients, steps,
                                    cooking_time, difficulty, servings, status, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (d.result['title'], d.result['description'], cat_id, d.result['ingredients'],
                  d.result['steps'], d.result['cooking_time'], d.result['difficulty'],
                  d.result['servings'], d.result['status'], d.result['tags']))

            messagebox.showinfo("成功", "✅ 菜谱创建成功！")
            self.refresh_all()

    def edit_recipe(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择要编辑的菜谱")
            return

        item = self.tree.item(sel[0])
        rid = item['values'][0]
        recipe = self.db.fetchone("SELECT * FROM recipes WHERE id=?", (rid,))

        if recipe:
            d = RecipeDialog(self.root, "编辑菜谱", recipe)
            if d.result:
                cat_id = None
                if d.result['category_name']:
                    c = self.db.fetchone("SELECT id FROM categories WHERE name=?", (d.result['category_name'],))
                    cat_id = c['id'] if c else None

                self.db.execute("""
                    UPDATE recipes SET title=?, description=?, category_id=?, ingredients=?,
                                       steps=?, cooking_time=?, difficulty=?, servings=?,
                                       status=?, tags=? WHERE id=?
                """, (d.result['title'], d.result['description'], cat_id, d.result['ingredients'],
                      d.result['steps'], d.result['cooking_time'], d.result['difficulty'],
                      d.result['servings'], d.result['status'], d.result['tags'], rid))

                messagebox.showinfo("成功", "✅ 菜谱已更新！")
                self.refresh_all()

    def delete_recipe(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择要删除的菜谱")
            return

        if messagebox.askyesno("确认", "确定要删除这个菜谱吗？"):
            item = self.tree.item(sel[0])
            rid = item['values'][0]
            self.db.execute("DELETE FROM recipes WHERE id=?", (rid,))
            messagebox.showinfo("成功", "✅ 菜谱已删除")
            self.refresh_all()

    def view_recipe(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择要查看的菜谱")
            return

        item = self.tree.item(sel[0])
        rid = item['values'][0]
        recipe = self.db.fetchone("SELECT * FROM recipes WHERE id=?", (rid,))

        if recipe:
            win = tk.Toplevel(self.root)
            win.title(f"📖 {recipe['title']}")
            win.geometry("600x500")

            f = ttk.Frame(win, padding=20)
            f.pack(fill=tk.BOTH, expand=True)

            ttk.Label(f, text=recipe['title'], font=('Arial', 18, 'bold')).pack(anchor=tk.W)
            ttk.Label(f, text=f"描述：{recipe['description'] or '无'}").pack(anchor=tk.W, pady=5)

            ttk.Separator(f).pack(fill=tk.X, pady=15)

            ttk.Label(f, text="【食材】", font=('Arial', 14, 'bold')).pack(anchor=tk.W)
            ing = tk.Text(f, height=5, wrap=tk.WORD)
            ing.pack(fill=tk.X, pady=5)
            ing.insert('1.0', recipe['ingredients'])
            ing.config(state='disabled')

            ttk.Label(f, text="【步骤】", font=('Arial', 14, 'bold')).pack(anchor=tk.W)
            stp = tk.Text(f, height=10, wrap=tk.WORD)
            stp.pack(fill=tk.BOTH, expand=True, pady=5)
            stp.insert('1.0', recipe['steps'])
            stp.config(state='disabled')

    def manage_categories(self):
        win = tk.Toplevel(self.root)
        win.title("🏷️ 类别管理")
        win.geometry("700x500")

        f = ttk.Frame(win, padding=20)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text="🏷️ 菜谱类别管理", font=('Arial', 16, 'bold')).pack(pady=(0, 15))

        cols = ('ID', '图标', '名称', '描述')
        tree = ttk.Treeview(f, columns=cols, show='headings', height=15)
        for col in cols:
            w = 60 if col == 'ID' else 150
            tree.heading(col, text=col)
            tree.column(col, width=w)

        tree.pack(fill=tk.BOTH, expand=True)

        def load():
            for i in tree.get_children():
                tree.delete(i)
            cats = self.db.fetchall("SELECT * FROM categories ORDER BY sort_order")
            for c in cats:
                tree.insert('', tk.END, values=(c['id'], c['icon'], c['name'], c['description']))

        def add_cat():
            d = CategoryDialog(self.root, "添加类别")
            if d.result:
                try:
                    self.db.execute("INSERT INTO categories (name, description, icon) VALUES (?, ?, ?)",
                                  (d.result['name'], d.result['description'], d.result['icon']))
                    load()
                except:
                    messagebox.showerror("错误", "类别名称已存在")

        def del_cat():
            sel = tree.selection()
            if not sel:
                return
            if messagebox.askyesno("确认", "确定删除？"):
                self.db.execute("DELETE FROM categories WHERE id=?", (tree.item(sel[0])['values'][0],))
                load()

        btnf = ttk.Frame(f)
        btnf.pack(pady=10)
        ttk.Button(btnf, text="➕ 添加", command=add_cat).pack(side=tk.LEFT, padx=5)
        ttk.Button(btnf, text="🗑️ 删除", command=del_cat).pack(side=tk.LEFT, padx=5)

        load()

    def search(self):
        win = tk.Toplevel(self.root)
        win.title("🔍 搜索菜谱")
        win.geometry("600x400")

        f = ttk.Frame(win, padding=20)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text="搜索关键词:").pack(anchor=tk.W)
        sv = tk.StringVar()
        e = ttk.Entry(f, textvariable=sv, width=50)
        e.pack(fill=tk.X, pady=(5, 10))

        result = tk.Text(f, height=15)
        result.pack(fill=tk.BOTH, expand=True)

        def do():
            k = sv.get()
            if not k: return
            rs = self.db.fetchall("SELECT * FROM recipes WHERE title LIKE ?", (f"%{k}%",))
            result.delete('1.0', tk.END)
            if rs:
                for r in rs:
                    result.insert(tk.END, f"📖 {r['title']}\n")
            else:
                result.insert(tk.END, "未找到结果")

        ttk.Button(f, text="搜索", command=do).pack(pady=5)
        e.bind('<Return>', lambda ev: do())
        e.focus()

    def do_search(self):
        self.search()

    def clear_search(self):
        self.search_var.set("")

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_recipes()

    def next_page(self):
        self.page += 1
        self.load_recipes()

    def add_defaults(self):
        defaults = [
            ('中餐', '🍜', '中式菜肴'), ('西餐', '🍝', '西式菜肴'),
            ('甜点', '🍰', '甜品点心'), ('饮品', '🥤', '饮料饮品'),
            ('沙拉', '🥗', '沙拉轻食'), ('汤品', '🍲', '汤类菜品'),
            ('快餐', '🍔', '快捷简餐'),
        ]
        count = 0
        for name, icon, desc in defaults:
            exists = self.db.fetchone("SELECT id FROM categories WHERE name=?", (name,))
            if not exists:
                self.db.execute("INSERT INTO categories (name, description, icon) VALUES (?, ?, ?)",
                              (name, desc, icon))
                count += 1
        messagebox.showinfo("成功", f"✅ 已添加 {count} 个默认类别")
        self.refresh_all()

    def on_closing(self):
        if messagebox.askokcancel("退出", "确定要退出吗？"):
            self.db.conn.close()
            self.root.destroy()

# ==================== 启动应用 ====================
if __name__ == "__main__":
    print("="*60)
    print(f"  {APP_NAME} {VERSION}")
    print("="*60)
    print("\n🚀 正在启动应用程序...\n")

    try:
        app = MenuApp()
        print("✅ 应用程序启动成功！")
        print("💡 提示：首次使用建议先添加默认类别\n")
        app.root.mainloop()
    except Exception as e:
        print(f"\n❌ 启动失败：{str(e)}\n")
        print("请检查:")
        print("1. Python 版本是否为 3.7+")
        print("2. 是否安装了 tkinter 库\n")
        input("按回车键退出...")
