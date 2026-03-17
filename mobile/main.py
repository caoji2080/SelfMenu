# 文件名：mobile/main.py
# 参考名称：00_应用主入口
# 说明：Flet 应用的启动入口

import sys
from pathlib import Path
import socket
import subprocess
import os

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from mobile.app import MenuApp


def check_and_free_port(port: int) -> bool:
    """检查并释放被占用的端口"""
    try:
        # 创建 socket 检测端口是否可用
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()

        if result == 0:
            print(f"⚠️  端口 {port} 被占用，尝试释放...")
            # Windows 系统查找占用端口的进程
            if os.name == 'nt':
                try:
                    # 使用 netstat 查找占用端口的 PID
                    cmd = f'netstat -ano | findstr :{port}'
                    output = subprocess.check_output(cmd, shell=True).decode('gbk')
                    for line in output.split('\n'):
                        if f':{port}' in line and 'LISTENING' in line:
                            parts = line.split()
                            if len(parts) > 4:
                                pid = parts[-1]
                                print(f"📌 发现占用进程 PID: {pid}")
                                # 尝试终止进程
                                subprocess.run(f'taskkill /PID {pid} /F',
                                             shell=True,
                                             capture_output=True)
                                print(f"✅ 已终止进程 {pid}")
                                return True
                except Exception as e:
                    print(f"⚠️  无法自动释放端口：{e}")
            return False
        return True
    except Exception as e:
        print(f"⚠️  端口检测失败：{e}")
        return True  # 检测失败时继续执行


def main(page: ft.Page):
    """应用入口函数"""
    app = MenuApp(page)
    page.add(app)
    page.update()


if __name__ == "__main__":
    PORT = 8550

    # 检查并释放端口
    check_and_free_port(PORT)

    # 使用 app() 方法 (Flet 0.23.0)
    print(f"🚀 正在启动 Flet 应用到端口 {PORT}...")
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=PORT)
