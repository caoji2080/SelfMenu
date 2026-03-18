# Filename: mobile/android_main.py
# Directory: D:\MenuApp\mobile\android_main.py
# Function: Android Buildozer App Entry Point with Logging

import sys
from pathlib import Path
import traceback
import logging
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup logging to file
log_file = Path(project_root) / "data" / "app.log"
try:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("=== App Starting ===")
except Exception as e:
    print(f"Could not setup logging: {e}")

import flet as ft
from mobile.app import MenuApp


def main(page: ft.Page):
    """Android app entry function with error display"""
    error_container = None

    try:
        # Configure page
        page.title = "Recipe Manager"
        page.bgcolor = "#F7F7F7"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT

        logging.info("Creating MenuApp instance...")

        # Create a loading indicator
        loading_text = ft.Text("Loading...", size=16, color=ft.colors.GREY_600)
        page.add(loading_text)
        page.update()

        # Create app instance
        logging.info("Creating MenuApp instance...")
        app = MenuApp(page)

        logging.info("Adding app to page...")
        page.controls.clear()
        page.add(app)

        logging.info("Updating page...")
        page.update()

        logging.info("✅ App loaded successfully!")

    except Exception as e:
        error_msg = traceback.format_exc()
        logging.error(f"❌ CRITICAL ERROR: {e}")
        logging.error(f"Stack trace:\n{error_msg}")

        # Display error to user
        try:
            if error_container is None:
                error_container = ft.Container(
                    content=ft.Column([
                        ft.Text("⚠️ App Startup Failed", size=20, weight="bold", color=ft.colors.RED),
                        ft.Divider(),
                        ft.Text(f"Error: {str(e)}", size=14, color=ft.colors.BLACK87),
                        ft.Text("", size=10),
                        ft.Text("Details (for developer):", size=12, weight="bold"),
                        ft.SelectableText(
                            error_msg[:500] + "..." if len(error_msg) > 500 else error_msg,
                            size=10,
                            bgcolor=ft.colors.GREY_200,
                        ),
                        ft.Divider(),
                        ft.Text("Log saved to: /data/data/com.menuapp/files/app.log", size=10, color=ft.colors.GREY_600),
                        ft.ElevatedButton(
                            "Try Again",
                            on_click=lambda _: page.route_refresh(),
                        ),
                    ], spacing=10),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    border=ft.border.all(2, ft.colors.RED_300),
                    margin=20,
                )

            page.controls.clear()
            page.add(error_container)
            page.update()
        except Exception as inner_e:
            logging.error(f"Failed to display error UI: {inner_e}")


if __name__ == "__main__":
    logging.info("Starting main execution...")
    try:
        ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)
    except Exception as e:
        logging.critical(f"Fatal error in ft.app: {e}")
        logging.critical(traceback.format_exc())
