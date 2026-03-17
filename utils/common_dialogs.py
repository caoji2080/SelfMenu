"""
通用对话框工具类
"""
import tkinter as tk
from tkinter import messagebox


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
