# 最简单的 Flet 测试文件

import flet as ft

def main(page: ft.Page):
    page.title = "测试页面"
    page.bgcolor = "#F7F7F7"

    # 添加简单内容
    page.add(
        ft.Text("Hello World!", size=30),
        ft.Container(
            content=ft.Text("这是一个测试"),
            bgcolor="blue",
            padding=20,
        ),
        ft.ElevatedButton("点击我", on_click=lambda e: print("按钮被点击了")),
    )

if __name__ == "__main__":
    ft.app(main, port=8551)
