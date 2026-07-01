import os

import flet as ft
from dotenv import load_dotenv

from database import fetch_saved_stories, delete_story_from_db

from auth import build_login_view, build_signup_view
from Screen.dashboard import build_dashboard_view
from Screen.song_generator import build_song_generate_view
from Screen.story_generator import build_story_generate_view
from AIScreen.ai_song_generator import build_song_ai_results_view
from AIScreen.ai_story_generator import build_story_ai_results_view
from Assistant import build_chat_assistant_view
from sidebar import build_sidebar
from home import build_home_page_view

load_dotenv()


def main(page: ft.Page):
    page.title = "Poet AI Studio"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 1250
    page.window_height = 800

    workspace_content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
    sidebar_layout = build_sidebar(lambda v: switch_workspace_view(v), "Dashboard")

    def switch_workspace_view(view_name: str):
        view_name = view_name.strip()
        workspace_content_area.controls.clear()

        sidebar_views = {
            "Dashboard",
            "Song Generate",
            "Song Generate-AI",
            "Generate Story",
            "Generate Story AI",
            "Chat Assistant",
        }

        sidebar_layout.visible = view_name in sidebar_views

        try:
            views = {
                "Home": build_home_page_view,
                "Dashboard": build_dashboard_view,
                "Song Generate": build_song_generate_view,
                "Song Generate-AI": build_song_ai_results_view,
                "Generate Story": build_story_generate_view,
                "Generate Story AI": build_story_ai_results_view,
                "Chat Assistant": build_chat_assistant_view,
                "Login": build_login_view,
                "Signup": build_signup_view,
            }

            if view_name in views:
                workspace_content_area.controls.append(
                    views[view_name](switch_workspace_view)
                )
            else:
                workspace_content_area.controls.append(
                    ft.Text(f"View '{view_name}' not found.", color="red")
                )

        except Exception as e:
            workspace_content_area.controls.append(
                ft.Text(f"Error loading {view_name}: {e}", color="red")
            )

        page.update()

    switch_workspace_view("Home")

    page.add(
        ft.Row(
            controls=[
                sidebar_layout,
                ft.Container(
                    content=workspace_content_area,
                    padding=40,
                    expand=True,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )


if __name__ == "__main__":
    port_number = int(os.getenv("PORT", "8000"))
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        host="127.0.0.1",
        port=port_number,
    )