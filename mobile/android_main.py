# Filename: mobile/android_main.py
# Directory: D:\MenuApp\mobile\android_main.py
# Function: Android Buildozer App Entry Point

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from mobile.app import MenuApp


def main(page: ft.Page):
    """Android app entry function"""
    try:
        # Configure page
        page.title = "Personal Recipe Management System"
        page.bgcolor = "#F7F7F7"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        print("🚀 Initializing application...")

        # Create app instance
        app = MenuApp(page)
        page.add(app)
        page.update()

        print("✅ Application loaded successfully")

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"❌ Application loading failed: {e}")
        print(f"Error details: {error_msg}")

        # Display error message to user
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Application Startup Failed", size=20, weight="bold"),
                    ft.Text(f"Error: {str(e)}", color=ft.colors.RED),
                    ft.Text("Please check logs or reinstall", size=12),
                ]),
                padding=20,
            )
        )
        page.update()


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)
