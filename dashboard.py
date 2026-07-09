import flet as ft


def create_dashboard_view(page: ft.Page, stats=None):
    """Create a polished dashboard experience for the app."""
    stats = stats or {}
    poems = stats.get("poems", 0)
    songs = stats.get("songs", 0)
    stories = stats.get("stories", 0)
    sessions = stats.get("sessions", 0)
    messages = stats.get("messages", 0)
    momentum = stats.get("momentum", 0)
    page_width = page.width or page.window_width or 1200

    def build_stat_card(icon_name, value, label, accent):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon_name, size=30, color=accent),
                    ft.Text(value, size=26, weight=ft.FontWeight.BOLD, color="#f8f8f2"),
                    ft.Text(label, size=13, color="#cceeee"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            bgcolor="#005f5f",
            padding=20,
            border_radius=16,
            width=180,
            height=140,
            shadow=ft.BoxShadow(color="#00000028", blur_radius=12, offset=ft.Offset(0, 4)),
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD, color="#f8f8f2"),
                            ft.Text("Track your creative writing milestones and stay inspired every day.", color="#d7f3f3", size=14),
                        ],
                        spacing=4,
                    ),
                    bgcolor="#004848",
                    padding=20,
                    width=max(page_width - 40, 280),
                    border_radius=8,
                    shadow=ft.BoxShadow(color="#00000025", blur_radius=10, offset=ft.Offset(0, 3)),
                ),
                ft.Container(height=16, width=100),
                ft.Row(
                    [
                        build_stat_card(ft.Icons.AUTO_AWESOME_ROUNDED, str(poems), "Poems Written", "#ffb74d"),
                        build_stat_card(ft.Icons.MUSIC_NOTE_ROUNDED, str(songs), "Songs Crafted", "#81c784"),
                        build_stat_card(ft.Icons.BOOK_ROUNDED, str(stories), "Stories Outlined", "#63b3ed"),
                        build_stat_card(ft.Icons.CHAT_BUBBLE_ROUNDED, str(sessions), "Chat Sessions", "#f472b6"),
                    ],
                    spacing=20,
                    wrap=True,
                ),
                ft.Container(height=18),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Creative Momentum", size=18, weight=ft.FontWeight.W_600, color="#f8f8f2"),
                            ft.Text(f"{messages} real messages across {sessions} chat sessions.", color="#d7f3f3", size=13),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Container(height=10, bgcolor="#ffb74d", width=max(12, int(2 * momentum)), border_radius=8),
                                        ft.Text(f"{momentum}%", color="#f8f8f2", size=12),
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                bgcolor="#006b6b",
                                padding=12,
                                border_radius=8,
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor="#005f5f",
                    padding=18,
                    border_radius=8,
                    shadow=ft.BoxShadow(color="#00000020", blur_radius=10, offset=ft.Offset(0, 3)),
                ),
                ft.Container(height=18),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LIGHTBULB_OUTLINED, color="#ffb74d", size=20),
                            ft.Text(
                                "Try mixing contrasting moods in your next song or story to create something unforgettable.",
                                size=13,
                                color="#eaf7f7",
                                max_lines=3,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor="#006b6b",
                    padding=15,
                    border_radius=14,
                ),
            ],
            expand=True,
            spacing=10,
        ),
        visible=False,
        expand=True,
    )
