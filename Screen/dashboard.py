import flet as ft
from database import fetch_saved_stories, delete_story_from_db
from session_store import SESSION

# --- DASHBOARD VIEW ---
def build_dashboard_view(nav_callback):

    user_id = SESSION.get("user_id")

    # 3. Simplify the access rule
    # If a user_id exists, we are authenticated, so fetch ONLY their data
    if user_id:
        saved_items = fetch_saved_stories(user_id=user_id)
    else:
        # GUEST mode: you can choose to show nothing or all stories
        saved_items = []

    saved_cards_row = ft.Row(wrap=True, spacing=20)

    # ---------------- CARD ----------------
    def create_card(sid, title, genre, content, timestamp):

        preview_snippet = (
            content[:65] + "..." if len(content) > 65 else content
        )

        # -------- VIEW DETAIL --------
        def open_detail_dialog(e):
            detail_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"📖 {title}", weight=ft.FontWeight.BOLD),
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Text(
                                    f"Genre: {genre}",
                                    size=12,
                                    color="#0D6E6E",
                                    weight=ft.FontWeight.W_600,
                                ),
                                bgcolor="#ECFEFF",
                                padding=8,
                                border_radius=8,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    content or "No content available.",
                                    size=13,
                                    color="#334155",
                                    selectable=True,
                                ),
                                width=520,
                                height=320,
                                padding=0,
                            ),
                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    width=560,
                    padding=0,
                ),
                actions=[
                    ft.TextButton(
                        "Close",
                        on_click=lambda ev: (
                            setattr(detail_dlg, "open", False),
                            e.page.update(),
                        ),
                    )
                ],
            )

            e.page.dialog = detail_dlg
            detail_dlg.open = True
            e.page.update()

        # -------- CARD UI (UNCHANGED STYLE) --------
        card = ft.Container(
            bgcolor="white",
            padding=16,
            border_radius=12,
            width=280,
            height=220,
            content=ft.Column(
                [
                    # HEADER
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.AUTO_STORIES,
                                        color="#0D6E6E",
                                        size=18,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            genre.upper(),
                                            size=10,
                                            color="white",
                                            weight="bold",
                                        ),
                                        bgcolor="#0D6E6E",
                                        padding=4,
                                        border_radius=4,
                                    ),
                                ]
                            ),

                            # ACTIONS
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.VISIBILITY_OUTLINED,
                                        icon_color="#0D6E6E",
                                        icon_size=18,
                                        tooltip="View Details",
                                        on_click=open_detail_dialog,
                                    ),

                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                        icon_color="#EF4444",
                                        icon_size=18,
                                        tooltip="Delete",
                                        on_click=lambda e: (
                                            delete_story_from_db(
                                                sid,
                                                SESSION.get("user_id")
                                            ),
                                            saved_cards_row.controls.remove(card),

                                            setattr(
                                                e.page,
                                                "snack_bar",
                                                ft.SnackBar(
                                                    ft.Text("🗑️ Deleted successfully")
                                                ),
                                            ),
                                            setattr(e.page.snack_bar, "open", True),
                                            e.page.update(),
                                        ),
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    # CONTENT
                    ft.GestureDetector(
                        on_tap=open_detail_dialog,
                        content=ft.Column(
                            [
                                ft.Text(
                                    title,
                                    size=14,
                                    weight="bold",
                                    color="#1E293B",
                                    max_lines=1,
                                ),
                                ft.Text(
                                    preview_snippet,
                                    size=12,
                                    color="#64748B",
                                ),
                            ]
                        ),
                    ),

                    # OPEN BUTTON
                    ft.ElevatedButton(
                        "Open in Chat",
                        icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                        on_click=lambda e: (
                            nav_callback("Song Generate")
                            if genre.lower() == "song"
                            else nav_callback("Generate Story")
                        ),
                    ),

                    ft.Text(
                        f"Saved: {str(timestamp)[:10]}",
                        size=10,
                        color="#94A3B8",
                        italic=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        return card

    # ---------------- EMPTY STATE ----------------
    if not saved_items:
        saved_cards_row.controls.append(
            ft.Text(
                "No saved items found. Start creating to populate your workspace!",
                size=13,
                color="#94A3B8",
                italic=True,
            )
        )
    else:
        for item in saved_items:
            saved_cards_row.controls.append(
                create_card(
                    item["id"],
                    item["title"],
                    item["genre"],
                    item["content"],
                    item["timestamp"],
                )
            )

    # ---------------- MAIN UI (UNCHANGED STYLE) ----------------
    return ft.ListView(
        [
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text(
                            "Welcome back, Creator",
                            size=28,
                            weight="bold",
                            color="#1E293B",
                        ),
                        ft.Text(
                            "Generate or continue your creative AI workflow.",
                            size=14,
                            color="#64748B",
                        ),

                        ft.Divider(height=15, color="transparent"),

                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Icon(ft.Icons.MUSIC_NOTE, color="#0D6E6E", size=28),
                                            ft.Text("Generate a Song", size=16, weight="bold"),
                                            ft.TextButton(
                                                "Launch Prompt",
                                                on_click=lambda e: nav_callback("Song Generate"),
                                            ),
                                        ]
                                    ),
                                    bgcolor="white",
                                    padding=20,
                                    border_radius=12,
                                    width=280,
                                    height=140,
                                ),

                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Icon(ft.Icons.BOOK, color="#0D6E6E", size=28),
                                            ft.Text("Write a Story", size=16, weight="bold"),
                                            ft.TextButton(
                                                "Launch Engine",
                                                on_click=lambda e: nav_callback("Generate Story"),
                                            ),
                                        ]
                                    ),
                                    bgcolor="white",
                                    padding=20,
                                    border_radius=12,
                                    width=280,
                                    height=140,
                                ),

                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Icon(ft.Icons.CHAT_BUBBLE, color="#0D6E6E", size=28),
                                            ft.Text("Chat Assistant", size=16, weight="bold"),
                                            ft.TextButton(
                                                "Launch Engine",
                                                on_click=lambda e: nav_callback("Chat Assistant"),
                                            ),
                                        ]
                                    ),
                                    bgcolor="white",
                                    padding=20,
                                    border_radius=12,
                                    width=280,
                                    height=140,
                                ),
                            ],
                            spacing=20,
                        ),

                        ft.Divider(height=25, color="transparent"),

                        ft.Text(
                            "Your Saved Project Artifacts Workspace",
                            size=18,
                            weight="bold",
                            color="#1E293B",
                        ),

                        saved_cards_row,
                    ]
                ),
            )
        ],
        expand=True,
    )