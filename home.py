import flet as ft
from responsive import ResponsiveConfig


def build_home_page_view(nav_callback):
    # Get responsive config - need to detect from page context
    # Since we don't have page access here, we'll use a reasonable default
    config = ResponsiveConfig(1200)  # Will be dynamic if called from page
    
    nav_padding = config.main_padding
    hero_padding = ft.padding.Padding(
        left=config.main_padding.left, 
        top=60 if config.is_mobile else 70,
        right=config.main_padding.right, 
        bottom=60 if config.is_mobile else 80
    )
    card_padding = config.card_padding

    website_header = ft.Container(
        content=ft.Row(
            [
                ft.Row([
                    ft.Icon(ft.Icons.AUTO_STORIES_ROUNDED, color="#0D6E6E", size=24 if not config.is_mobile else 20),
                    ft.Text("Poet AI", size=18 if not config.is_mobile else 16, weight=ft.FontWeight.BOLD, color="#1E293B"),
                ], spacing=8),
                ft.Row([
                    ft.TextButton("Features", style=ft.ButtonStyle(color="#64748B")),
                    ft.TextButton("Pricing", style=ft.ButtonStyle(color="#64748B")),
                    ft.ElevatedButton("Signup", bgcolor="#0D6E6E", color="white", on_click=lambda _: nav_callback("Login")),
                ], spacing=15 if not config.is_mobile else 8, wrap=config.is_mobile),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            wrap=config.is_mobile,
        ),
        padding=nav_padding,
        border=ft.Border(bottom=ft.BorderSide(1, "#E2E8F0")),
        bgcolor="white",
    )

    hero_headline = ft.Text(
        "Where Human Creativity\nMeets Advanced AI",
        size=config.heading_size,
        weight=ft.FontWeight.BOLD,
        color="#1E293B",
        text_align=ft.TextAlign.CENTER,
    )
    hero_subtext = ft.Text(
        "Create songs, stories, and polished ideas in one playful workspace with a calm, guided experience.",
        size=config.body_text_size,
        color="#64748B",
        text_align=ft.TextAlign.CENTER,
    )

    hero_action_buttons = ft.Row(
        [
            ft.ElevatedButton(
                "Start Creating Free", 
                bgcolor="#0D6E6E", 
                color="white", 
                width=config.button_width, 
                height=config.button_height, 
                on_click=lambda _: nav_callback("Signup")
            ),
            ft.OutlinedButton(
                "Explore Workspace", 
                style=ft.ButtonStyle(color="#0D6E6E"), 
                width=config.button_width, 
                height=config.button_height, 
                on_click=lambda _: nav_callback("Login")
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=config.spacing_medium,
        wrap=config.is_mobile,
    )

    hero_section = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("✨ NOW IN BETA — POWERED BY GEMINI 2.5 FLASH", size=10 if config.is_mobile else 11, color="#0D6E6E", weight=ft.FontWeight.W_600),
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
            spacing=config.spacing_large,
        ),
        padding=hero_padding,
        animate=ft.Animation(400, curve=ft.AnimationCurve.DECELERATE),
    )

    def create_feature_card(icon, title, desc):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color="#0D6E6E", size=32 if not config.is_mobile else 28),
                ft.Text(title, size=config.subheading_size, weight=ft.FontWeight.BOLD, color="#1E293B"),
                ft.Text(desc, size=config.body_text_size, color="#64748B"),
            ], spacing=8, alignment=ft.MainAxisAlignment.START),
            bgcolor="white",
            padding=card_padding,
            border_radius=14,
            width=config.card_width,
            height=150 if not config.is_mobile else None,
            shadow=ft.BoxShadow(blur_radius=20, color="#00000010", offset=ft.Offset(0, 4)),
            border=ft.Border.all(1, "#E2E8F0"),
            animate=ft.Animation(300, curve=ft.AnimationCurve.DECELERATE),
        )

    features_row = ft.Row([
        create_feature_card(ft.Icons.MUSIC_NOTE_ROUNDED, "Lyric Studio", "Create polished multi-turn song drafts with a guided, collaborative flow."),
        create_feature_card(ft.Icons.AUTO_STORIES_ROUNDED, "Story Lab", "Shape characters, scenes, and twists into a complete narrative arc."),
        create_feature_card(ft.Icons.DASHBOARD_ROUNDED, "Creative Vault", "Save your favorite outputs locally and revisit them whenever inspiration returns."),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=config.spacing_large, wrap=True)

    website_layout_scroll_area = ft.Column(
        [
            website_header,
            hero_section,
            ft.Text("DESIGNED FOR MODERN AUTHORS AND MUSIC MAKERS", size=11 if config.is_mobile else 12, color="#94A3B8", weight=ft.FontWeight.BOLD),
            ft.Divider(height=6, color="transparent"),
            features_row,
            ft.Divider(height=40, color="transparent"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=config.spacing_medium,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.Container(content=website_layout_scroll_area, expand=True, bgcolor="#F8FAFC")
