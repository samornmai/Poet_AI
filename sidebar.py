import flet as ft

def build_sidebar(switch_workspace_view, current_active_label="Dashboard", current_user_role="User"):
    DARK_CYAN = "#0D6E6E"
    
    # Text container component holding your navigation links row reference array
    menu_items = ft.Column(spacing=4)

    # --- SIDEBAR NAV SELECTION LISTENER ---
    def menu_clicked(e):
        # Reset background colors and states of all navigation container options
        for btn in menu_items.controls:
            if isinstance(btn, ft.Container) and hasattr(btn, "on_click") and btn.on_click is not None:
                btn.bgcolor = "transparent"
                # Safely loop through inner control children row lists to dim down texts/icons uniformly
                if btn.content and hasattr(btn.content, "controls"):
                    for control in btn.content.controls:
                        if isinstance(control, ft.Text):
                            control.color = "white74"
                        elif isinstance(control, ft.Icon):
                            control.color = "white74"
                
        # Highlight clicked item container background color
        e.control.bgcolor = "rgba(255,255,255,0.12)"
        # Safely loop through inner control children row lists to highlight active choices cleanly
        if e.control.content and hasattr(e.control.content, "controls"):
            for control in e.control.content.controls:
                if isinstance(control, ft.Text):
                    control.color = "white"
                elif isinstance(control, ft.Icon):
                    control.color = "white"
        
        # Map user-friendly labels cleanly to view names via metadata storage
        clicked_route = e.control.data
        switch_workspace_view(clicked_route)

    # Helper utility to build navigation entries uniformly with enhanced interactive styles
    def create_menu_button(icon, display_label, router_route_name):
        is_active = (router_route_name == current_active_label or display_label == current_active_label)
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="white" if is_active else "white74", size=18),
                ft.Text(display_label, color="white" if is_active else "white74", weight=ft.FontWeight.W_500, size=13)
            ], alignment=ft.MainAxisAlignment.START, spacing=12),
            padding=ft.padding.Padding(left=14, top=10, right=14, bottom=10),
            border_radius=8,
            bgcolor="rgba(255,255,255,0.12)" if is_active else "transparent",
            on_click=menu_clicked,
            data=router_route_name  # Binds the exact router string token cleanly to metadata storage
        )

    # Helper utility to draw clean, semantic text subsection categorizers
    def create_section_header(title_text):
        return ft.Container(
            content=ft.Text(title_text, color="white45", size=10, weight=ft.FontWeight.BOLD),
            padding=ft.padding.Padding(left=14, top=16, right=0, bottom=6)
        )

    # Populate the navigation menu with core workspace tools
    menu_items.controls.extend([
        create_section_header("CORE WORKSPACE"),
        create_menu_button(ft.Icons.DASHBOARD_ROUNDED, "Project Dashboard", "Dashboard"),
        create_menu_button(ft.Icons.MUSIC_NOTE_ROUNDED, "Lyrics Generator", "Song Generate"),
        create_menu_button(ft.Icons.BOOK_ROUNDED, "Story Scriptorium", "Generate Story")
    ])

    # --- CONDITIONAL ADMIN ONLY CONTROLS ---
    # Only reveal the user management panel if the logged-in profile is verified as an Admin
    if current_user_role == "Admin":
        menu_items.controls.extend([
            create_section_header("ADMINISTRATOR"),
            create_menu_button(ft.Icons.SUPERVISOR_ACCOUNT_ROUNDED, "User Management", "Create User")
        ])

    # --- SIDEBAR INTERFACE LAYOUT STRUCTURE ---
    sidebar_header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.AUTO_STORIES, color="white", size=18), 
                bgcolor="rgba(255,255,255,0.18)", 
                padding=8, 
                border_radius=8
            ),
            ft.Column([
                ft.Text("Poet AI", color="white", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Studio Suite v2.5", color="white54", size=10, weight=ft.FontWeight.W_400)
            ], spacing=1)
        ], spacing=10),
        padding=ft.padding.Padding(left=0, top=0, right=0, bottom=20),
        border=ft.Border(bottom=ft.BorderSide(1, "rgba(255,255,255,0.08)"))
    )

    # Dynamically scale user profile subtitle display values depending on authorization parameters
    role_badge = "System Administrator" if current_user_role == "Admin" else "Free Hobby Plan"

    sidebar_footer = ft.Container(
        content=ft.Row([
            ft.Row([
                # FIXED: Swapped out RAW_FLEX_ROUNDED for ADMIN_PANEL_SETTINGS_ROUNDED
                ft.CircleAvatar(
                    content=ft.Icon(
                        ft.Icons.PERSON if current_user_role != "Admin" else ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, 
                        color="white", 
                        size=18
                    ), 
                    bgcolor="rgba(255,255,255,0.15)", 
                    radius=18
                ),
                ft.Column([
                    ft.Text("Creator Account", color="white", size=13, weight=ft.FontWeight.W_600),
                    ft.Text(role_badge, color="white60", size=10)
                ], spacing=1)
            ], spacing=10, expand=True),
            
            ft.IconButton(
                icon=ft.Icons.LOGOUT_ROUNDED,
                icon_color="white54",
                icon_size=16,
                tooltip="Log Out and Exit Workspace",
                on_click=lambda _: switch_workspace_view("Home")
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.Padding(left=0, top=16, right=0, bottom=0),
        border=ft.Border(top=ft.BorderSide(1, "rgba(255,255,255,0.08)"))
    )

    return ft.Container(
        content=ft.Column([
            sidebar_header, 
            ft.Container(content=menu_items, expand=True), 
            sidebar_footer
        ]),
        width=260, 
        bgcolor=DARK_CYAN, 
        padding=20,
    )