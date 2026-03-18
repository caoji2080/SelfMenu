# Filename: mobile/android_main.py
# Directory: D:\MenuApp\mobile\android_main.py
# Function: Android Buildozer App Entry Point

import sys
from pathlib import Path
import traceback

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from mobile.app import MenuApp


def main(page: ft.Page):
    """Android app entry function"""
    try:
        # Configure page
        page.title = "Recipe Manager"
        page.bgcolor = "#F7F7F7"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        print("=" * 50)
        print("Starting Recipe Manager App...")
        print("=" * 50)

        # Create app instance
        print("Creating MenuApp instance...")
        app = MenuApp(page)

        print("Adding app to page...")
        page.add(app)

        print("Updating page...")
        page.update()

        print("=" * 50)
        print("App loaded successfully!")
        print("=" * 50)

    except Exception as e:
        error_msg = traceback.format_exc()
        print("=" * 50)
        print(f"CRITICAL ERROR: {e}")
        print("=" * 50)
        print("Stack trace:")
        print(error_msg)

        # Display error to user
        try:
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("App Startup Failed", size=20, weight="bold"),
                        ft.Text(f"Error: {str(e)}", color=ft.colors.RED, size=14),
                        ft.Text("Please check logcat for details", size=12),
                    ]),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                )
            )
            page.update()
        except:
            pass


if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)
