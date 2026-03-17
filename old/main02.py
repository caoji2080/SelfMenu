
"""
个人菜谱管理系统 - 主启动文件
"""
import sys
import tkinter as tk
from tkinter import messagebox


def check_dependencies():
    """检查依赖"""
    required_modules = ['tkinter', 'sqlite3', 'pathlib', 'datetime', 'json', 'csv']
    missing = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        msg = f"缺少必要的模块：{', '.join(missing)}\n请安装后再运行"
        messagebox.showerror("依赖缺失", msg)
        return False

    return True


def main():
    """主函数"""
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 打印启动信息
    print("=" * 60)
    print("  🍳 个人菜谱管理系统 v1.0.0")
    print("=" * 60)
    print("\n🚀 正在启动应用程序...\n")

    try:
        # 导入并创建应用启动器
        from launcher import ApplicationLauncher

        launcher = ApplicationLauncher()
        launcher.launch()

        print("✅ 应用程序启动成功！")

    except Exception as e:
        print(f"\n❌ 启动失败：{str(e)}\n")
        print("请检查:")
        print("1. Python 版本是否为 3.7+")
        print("2. 是否安装了 tkinter 库")
        print("3. 数据库文件是否正常\n")
        input("按回车键退出...")


if __name__ == "__main__":
    main()
