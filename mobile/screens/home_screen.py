# Filename: mobile/screens/home_screen.py
# Directory: D:\MenuApp\mobile\screens\home_screen.py
# Function: App Home Screen - Welcome message and quick actions

import flet as ft
from datetime import datetime


class HomeScreen(ft.Container):
    """Home screen - Main landing page"""

    def __init__(self, on_navigate, recipe_service, category_service):
        super().__init__()
        self.on_navigate = on_navigate
        self.recipe_service = recipe_service
        self.category_service = category_service
        self.recipe_count = 0
        self.category_count = 0
        self.favorite_count = 0
        self.recent_recipes = []
        self.expand = True

        # Build UI lazily in did_mount
        self.content = ft.Column([
            ft.Container(
                content=ft.Text("Loading...", size=16),
                padding=20,
            )
        ])

    def did_mount(self):
        """Called after component is mounted"""
        print("Home screen mounted, building UI...")
        self.content = self._build_ui()
        self.update()
        print("Home screen UI built successfully")

    def _build_ui(self):
        """Build the UI"""
        # Get statistics safely
        try:
            all_recipes = self.recipe_service.get_all_recipes()
            all_categories = self.category_service.get_all_categories()
            self.recipe_count = len(all_recipes) if all_recipes else 0
            self.category_count = len(all_categories) if all_categories else 0
            self.favorite_count = 0

            # Get recent recipes
            if all_recipes:
                sorted_recipes = sorted(
                    all_recipes,
                    key=lambda r: r.updated_at or r.created_at or '',
                    reverse=True
                )
                self.recent_recipes = sorted_recipes[:2]
            else:
                self.recent_recipes = []
        except Exception as e:
            print(f"Error getting data: {e}")
            self.recipe_count = 0
            self.category_count = 0
            self.favorite_count = 0
            self.recent_recipes = []

        hour = datetime.now().hour
        greeting = "Good Morning" if hour < 12 else ("Good Afternoon" if hour < 18 else "Good Evening")

        return ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("[icon]", size=32),
                        ft.Text("Recipe Manager", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ], alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                    bgcolor="#FF6B6B",
                    border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
                ),

                # Welcome
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{greeting}!", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                        ft.Text(
                            f"{datetime.now().strftime('%Y-%m-%d')}",
                            size=14,
                            color=ft.colors.GREY_700,
                        ),
                    ], spacing=5),
                    padding=20,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#FFE5E5", "#FFF0F0"],
                    ),
                    border_radius=15,
                    margin=ft.margin.symmetric(horizontal=15, vertical=10),
                ),

                # Stats cards
                ft.Container(
                    content=ft.Row([
                        self._create_stat_card("[icon]", "Recipes", str(self.recipe_count), "#E3F2FD", "/recipes"),
                        self._create_stat_card("[icon]", "Categories", str(self.category_count), "#E8F5E9", "/categories"),
                        self._create_stat_card("[star]", "Favorites", str(self.favorite_count), "#FFF3E0", "/favorites"),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=15,
                    margin=ft.margin.symmetric(horizontal=15, vertical=5),
                ),

                # Quick actions
                ft.Container(
                    content=ft.Text("Quick Actions", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                    padding=ft.padding.only(left=15, top=10, bottom=5),
                ),

                ft.Container(
                    content=ft.Row([
                        self._create_action_button("[edit]", "New Recipe", "/new_recipe"),
                        self._create_action_button("[search]", "Search", "/search"),
                        self._create_action_button("[label]", "Categories", "/categories"),
                        self._create_action_button("[upload]", "Import/Export", "/import_export"),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=15,
                ),

                # Recent recipes
                ft.Container(
                    content=ft.Row([
                        ft.Text("Recent Recipes", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                        ft.TextButton(
                            "View All >",
                            on_click=lambda e: self.on_navigate("/recipes"),
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.only(left=15, top=10, bottom=5),
                ),

                self._create_recent_recipes_list(),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
        )

    def _create_recent_recipes_list(self):
        """Create recent recipes list"""
        if not self.recent_recipes:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.RESTAURANT_MENU, size=60, color=ft.colors.GREY_400),
                    ft.Text("No recipes yet", size=14, color=ft.colors.GREY_600),
                    ft.Text("Click 'New Recipe' to create your first recipe!", size=12, color=ft.colors.GREY_500),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=40,
                bgcolor=ft.colors.GREY_100,
                border_radius=10,
                margin=ft.margin.symmetric(horizontal=15, vertical=5),
            )

        recipe_cards = []
        for recipe in self.recent_recipes:
            card = self._create_recent_recipe_card(recipe)
            recipe_cards.append(card)

        return ft.Container(
            content=ft.Column(
                controls=recipe_cards,
                spacing=10,
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
        )

    def _create_recent_recipe_card(self, recipe):
        """Create recipe card"""
        update_time = recipe.updated_at or recipe.created_at or 'Unknown'
        if len(update_time) > 16:
            update_time = update_time[:16].replace('T', ' ')

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"#{recipe.id}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    width=50,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(recipe.title, size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                        ft.Row([
                            ft.Icon(ft.icons.LABEL_OUTLINE, size=14, color=ft.colors.GREY_600),
                            ft.Text(recipe.category_name or "Uncategorized", size=12, color=ft.colors.GREY_600),
                        ], spacing=5),
                    ], spacing=5),
                    expand=True,
                    padding=ft.padding.only(right=10),
                ),
                ft.Icon(ft.icons.CHEVRON_RIGHT, color=ft.colors.GREY_400),
            ], alignment=ft.MainAxisAlignment.START),
            padding=15,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            on_click=lambda e, r=recipe: self.on_recipe_click(r),
            ink=True,
        )

    def on_recipe_click(self, recipe):
        """Handle recipe click"""
        route = f"/recipe/{recipe.id}"
        print(f"Recipe clicked: {route}")
        self.on_navigate(route, recipe_id=recipe.id)

    def _create_stat_card(self, icon: str, label: str, value: str, bgcolor: str, navigate_route: str):
        """Create stat card"""
        return ft.Container(
            content=ft.Column([
                ft.Text(icon, size=28),
                ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87),
                ft.Text(label, size=12, color=ft.colors.GREY_700),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=15,
            bgcolor=bgcolor,
            border_radius=10,
            width=100,
            on_click=lambda e: self._handle_stat_click(navigate_route),
            ink=True,
        )

    def _handle_stat_click(self, route: str):
        """Handle stat card click"""
        print(f"Stat card clicked: {route}")
        if route == "/favorites":
            print("Favorites feature not implemented yet")
            return
        self.on_navigate(route)

    def _create_action_button(self, icon: str, label: str, route: str):
        """Create action button"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(icon, size=32),
                    padding=15,
                    bgcolor=ft.colors.GREY_200,
                    border_radius=50,
                    width=70,
                    height=70,
                    alignment=ft.alignment.center,
                ),
                ft.Text(label, size=12, color=ft.colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            on_click=lambda e: self.on_navigate(route),
            padding=10,
            width=90,
        )
