import flet as ft
from database import fetch_saved_stories, delete_story_from_db
from session_store import SESSION
from responsive import ResponsiveConfig

# --- DASHBOARD VIEW ---
def build_dashboard_view(nav_callback):

    user_id = SESSION.get("user_id")
    config = ResponsiveConfig(1200)  # Default, adapts with responsive system

    # 3. Simplify the access rule
    # If a user_id exists, we are authenticated, so fetch ONLY their data
    if user_id:
        saved_items = fetch_saved_stories(user_id=user_id)
    else:
        # GUEST mode: you can choose to show nothing or all stories
        saved_items = []

    saved_cards_row = ft.Row(wrap=True, spacing=config.spacing_large)

    # ---------------- CARD ----------------
    def create_card(sid, title, genre, content, timestamp):

        preview_snippet = (
            content[:65] + "..." if len(content) > 65 else content
        )

        # -------- VIEW DETAIL --------
        def open_detail_dialog(e):
            dialog_width = 560 if not config.is_mobile else 320
            dialog_height = 320 if not config.is_mobile else 400
            
            detail_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"📖 {title}", weight=ft.FontWeight.BOLD, size=config.subheading_size),
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Text(
                                    f"Genre: {genre}",
                                    size=config.body_text_size,
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
                                    size=config.body_text_size,
                                    color="#334155",
                                    selectable=True,
                                ),
                                width=dialog_width - 40,
                                height=dialog_height,
                                padding=0,
                            ),
                        ],
                        spacing=config.spacing_medium,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    width=dialog_width,
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

        # -------- CARD UI (RESPONSIVE STYLE) --------
        card = ft.Container(
            bgcolor="white",
            padding=config.card_padding,
            border_radius=12,
            width=config.card_width,
            height=220 if not config.is_mobile else None,
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
                                    size=config.body_text_size,
                                    color="#64748B",
                                ),
                            ]
                        ),
                    ),

                    # OPEN BUTTON
                    ft.ElevatedButton(
                        "Open in Chat",
                        icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                        width=config.button_width,
                        height=config.button_height,
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
                size=config.body_text_size,
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

    # ----------- QUICK ACTION BUTTONS ---------
    quick_action_buttons = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.MUSIC_NOTE, color="#0D6E6E", size=28),
                        ft.Text("Generate a Song", size=config.subheading_size, weight="bold"),
                        ft.TextButton(
                            "Launch Prompt",
                            on_click=lambda e: nav_callback("Song Generate"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=config.card_padding,
                bgcolor="white",
                border_radius=12,
                width=config.card_width,
                border=ft.Border.all(1, "#E2E8F0"),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.AUTO_STORIES, color="#0D6E6E", size=28),
                        ft.Text("Generate a Story", size=config.subheading_size, weight="bold"),
                        ft.TextButton(
                            "Launch Prompt",
                            on_click=lambda e: nav_callback("Generate Story"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=config.card_padding,
                bgcolor="white",
                border_radius=12,
                width=config.card_width,
                border=ft.Border.all(1, "#E2E8F0"),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.CHAT_BUBBLE, color="#0D6E6E", size=28),
                        ft.Text("Chat Assistant", size=config.subheading_size, weight="bold"),
                        ft.TextButton(
                            "Launch Engine",
                            on_click=lambda e: nav_callback("Chat Assistant"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=config.card_padding,
                bgcolor="white",
                border_radius=12,
                width=config.card_width,
                border=ft.Border.all(1, "#E2E8F0"),
            ),
        ],
        wrap=True,
        spacing=config.spacing_large,
    )

    # -------- MAIN UI (RESPONSIVE) --------
    return ft.ListView(
        [
            ft.Container(
                padding=config.main_padding,
                content=ft.Column(
                    [
                        ft.Text(
                            "Welcome back, Creator",
                            size=config.heading_size,
                            weight="bold",
                            color="#1E293B",
                        ),
                        ft.Text(
                            "Generate or continue your creative AI workflow.",
                            size=config.body_text_size,
                            color="#64748B",
                        ),

                        ft.Divider(height=15, color="transparent"),
                        
                        quick_action_buttons,

                        ft.Divider(height=25, color="transparent"),

                        ft.Text(
                            "Your Saved Project Artifacts Workspace",
                            size=config.subheading_size,
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