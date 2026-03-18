# Filename: mobile/android_main.py
# Directory: D:\MenuApp\mobile\android_main.py
# Function: Minimal Android Entry Point for Testing

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import flet as ft


def main(page: ft.Page):
    """Minimal test app - no dependencies"""
    try:
        # Basic page setup
        page.title = "Recipe Manager Test"
        page.bgcolor = "#FFFFFF"
        page.padding = 20
        page.theme_mode = ft.ThemeMode.LIGHT

        print("=" * 60)
        print("🚀 TEST APP STARTING")
        print("=" * 60)

        # Simple test content
        test_text = ft.Text(
            "✅ App Started Successfully!\n\n"
            "If you can see this, the basic app works.\n\n"
            "Next step: Load full MenuApp...",
            size=16,
            text_align=ft.TextAlign.CENTER,
        )

        page.add(test_text)
        page.update()

        print("✅ Basic UI displayed")
        print("=" * 60)

        # Try to import and load full app after 2 seconds
        def load_full_app(e):
            try:
                page.controls.clear()
                page.add(ft.Text("Loading full app...", size=16))
                page.update()

                from mobile.app import MenuApp
                app = MenuApp(page)
                page.controls.clear()
                page.add(app)
                page.update()

                print("✅ Full app loaded")
            except Exception as e:
                import traceback
                error_msg = traceback.format_exc()
                print(f"❌ Error loading full app: {e}")
                print(error_msg)

                page.controls.clear()
                page.add(
                    ft.Column([
                        ft.Text("⚠️ Error Loading Full App",
                               size=18, color=ft.colors.RED, weight="bold"),
                        ft.Divider(),
                        ft.Text(f"Error: {str(e)}", size=12),
                        ft.SelectableText(
                            error_msg[:800] if len(error_msg) > 800 else error_msg,
                            size=10,
                            bgcolor=ft.colors.GREY_200,
                        ),
                        ft.ElevatedButton("Retry", on_click=load_full_app),
                    ])
                )
                page.update()

        # Add button to manually trigger full app load
        page.add(
            ft.ElevatedButton(
                "Load Full MenuApp",
                on_click=load_full_app,
                style=ft.ButtonStyle(
                    padding=20,
                    bgcolor=ft.colors.BLUE,
                ),
            )
        )

        print("✅ Test app ready - click button to load full app")
        print("=" * 60)

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"❌ CRITICAL ERROR in main(): {e}")
        print(error_msg)

        # This might not display if error is too early
        try:
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("💥 Fatal Error", size=20, color=ft.colors.RED),
                        ft.Text(str(e), size=14),
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=20,
                )
            )
        except:
            pass


if __name__ == "__main__":
    print("🔹 android_main.py executed")
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)
