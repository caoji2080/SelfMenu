
"""
应用启动器 - 负责应用的初始化和启动
"""
import tkinter as tk
from tkinter import messagebox
import sys
import traceback


class ApplicationLauncher:
    """应用启动器"""

    def __init__(self):
        self.root = None
        self.app = None

    def launch(self):
        """启动应用"""
        try:
            # 创建主窗口
            self.root = tk.Tk()
            self.root.title("个人菜谱管理系统 v1.0.0")
            self.root.geometry("1200x800")

            # 设置窗口图标（如果有）
            try:
                self.root.iconbitmap('icon.ico')
            except:
                pass

            # 创建并初始化应用
            from services.recipe_service import RecipeService
            from services.category_service import CategoryService

            recipe_service = RecipeService()
            category_service = CategoryService()

            # 创建主界面
            from views.main_view import MainApplication
            self.app = MainApplication(self.root, recipe_service, category_service)

            # 启动主循环
            self.root.mainloop()

        except Exception as e:
            self._handle_startup_error(e)

    def _handle_startup_error(self, error: Exception):
        """处理启动错误"""
        error_msg = f"""
应用启动失败！

错误信息：{str(error)}
错误类型：{type(error).__name__}

可能的原因:
1. Python 版本不是 3.7+
2. 缺少必要的依赖库 (tkinter)
3. 数据库文件损坏
4. 权限不足

详细错误信息:
{traceback.format_exc()}
        """

        print(error_msg)
        messagebox.showerror("启动失败", error_msg)
        sys.exit(1)


def main():
    """主函数"""
    launcher = ApplicationLauncher()
    launcher.launch()


if __name__ == "__main__":
    main()
