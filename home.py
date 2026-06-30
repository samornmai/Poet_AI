import flet as ft


def build_home_page_view(nav_callback):
    nav_padding = ft.padding.Padding(left=40, top=16, right=40, bottom=16)
    hero_padding = ft.padding.Padding(left=40, top=70, right=40, bottom=80)
    card_padding = ft.padding.Padding(left=24, top=24, right=24, bottom=24)

    website_header = ft.Container(
        content=ft.Row(
            [
                ft.Row([
                    ft.Icon(ft.Icons.AUTO_STORIES_ROUNDED, color="#0D6E6E", size=24),
                    ft.Text("Poet AI", size=18, weight=ft.FontWeight.BOLD, color="#1E293B"),
                ], spacing=8),
                ft.Row([
                    ft.TextButton("Features", style=ft.ButtonStyle(color="#64748B")),
                    ft.TextButton("Pricing", style=ft.ButtonStyle(color="#64748B")),
                    ft.ElevatedButton("Signup", bgcolor="#0D6E6E", color="white", on_click=lambda _: nav_callback("Login")),
                ], spacing=15),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=nav_padding,
        border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
        bgcolor="white",
    )

    hero_headline = ft.Text(
        "Where Human Creativity\nMeets Advanced AI",
        size=46,
        weight=ft.FontWeight.BOLD,
        color="#1E293B",
        text_align=ft.TextAlign.CENTER,
    )
    hero_subtext = ft.Text(
        "Create songs, stories, and polished ideas in one playful workspace with a calm, guided experience.",
        size=15,
        color="#64748B",
        text_align=ft.TextAlign.CENTER,
    )

    hero_action_buttons = ft.Row(
        [
            ft.ElevatedButton("Start Creating Free", bgcolor="#0D6E6E", color="white", width=220, height=50, on_click=lambda _: nav_callback("Signup")),
            ft.OutlinedButton("Explore Workspace", style=ft.ButtonStyle(color="#0D6E6E"), width=220, height=50, on_click=lambda _: nav_callback("Login")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    hero_section = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("✨ NOW IN BETA — POWERED BY GEMINI 2.5 FLASH", size=11, color="#0D6E6E", weight=ft.FontWeight.W_600),
                    bgcolor="rgba(13, 110, 110, 0.1)",
                    padding=ft.padding.Padding(left=12, top=6, right=12, bottom=6),
                    border_radius=20,
                ),
                hero_headline,
                hero_subtext,
                ft.Divider(height=10, color="transparent"),
                hero_action_buttons,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
        ),
        padding=hero_padding,
        animate=ft.Animation(400, curve=ft.AnimationCurve.DECELERATE),
    )

    def create_feature_card(icon, title, desc):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color="#0D6E6E", size=32),
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="#1E293B"),
                ft.Text(desc, size=13, color="#64748B"),
            ], spacing=8, alignment=ft.MainAxisAlignment.START),
            bgcolor="white",
            padding=card_padding,
            border_radius=14,
            width=280,
            height=150,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000010", offset=ft.Offset(0, 4)),
            border=ft.Border.all(1, "#E2E8F0"),
            animate=ft.Animation(300, curve=ft.AnimationCurve.DECELERATE),
        )

    features_row = ft.Row([
        create_feature_card(ft.Icons.MUSIC_NOTE_ROUNDED, "Lyric Studio", "Create polished multi-turn song drafts with a guided, collaborative flow."),
        create_feature_card(ft.Icons.AUTO_STORIES_ROUNDED, "Story Lab", "Shape characters, scenes, and twists into a complete narrative arc."),
        create_feature_card(ft.Icons.DASHBOARD_ROUNDED, "Creative Vault", "Save your favorite outputs locally and revisit them whenever inspiration returns."),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=24)

    website_layout_scroll_area = ft.Column(
        [
            website_header,
            hero_section,
            ft.Text("DESIGNED FOR MODERN AUTHORS AND MUSIC MAKERS", size=12, color="#94A3B8", weight=ft.FontWeight.BOLD),
            ft.Divider(height=6, color="transparent"),
            features_row,
            ft.Divider(height=40, color="transparent"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.Container(content=website_layout_scroll_area, expand=True, bgcolor="#F8FAFC")
