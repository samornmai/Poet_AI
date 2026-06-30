import flet as ft

# Global memory to hold selections safely across screen refreshes
song_parameters = {"genre": "", "theme": "", "nuance": ""}

def build_song_generate_view(nav_callback):
    # Safe legacy padding initialization
    card_padding = ft.padding.Padding(left=28, top=28, right=28, bottom=28)
    
    # --- FORM INPUT CONTROLS CONFIGURATION ---
    genre_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Pop Rock Track"), 
            ft.dropdown.Option("Synthwave Beats"), 
            ft.dropdown.Option("Acoustic Indie Ballad"),
            ft.dropdown.Option("Hip-Hop / Rap Verse"),
            ft.dropdown.Option("Cinematic Orchestral")
        ],
        hint_text="Choose a musical landscape...",
        width=500, 
        bgcolor="#F8FAFC", 
        border_radius=8,
        border_color="#CBD5E1"
    )
    
    theme_input = ft.TextField(
        hint_text="Describe the story, mood, or narrative concept (e.g., A rainy night in Tokyo, moving on from past mistakes)...", 
        multiline=True, 
        min_lines=3, 
        max_lines=4, 
        width=500, 
        bgcolor="#F8FAFC",
        border_radius=8,
        border_color="#CBD5E1",
        content_padding=12
    )
    
    nuance_input = ft.TextField(
        hint_text="e.g., Nostalgic guitar solos, high-energy 80s synths, bittersweet, melancholic", 
        width=500, 
        bgcolor="#F8FAFC",
        border_radius=8,
        border_color="#CBD5E1"
    )

    # --- ACTION SUBMIT ROUTING CONTEXT ---
    def submit_data(e):
        # Fallback safe defaults if user leaves field slots empty
        song_parameters["genre"] = genre_dropdown.value or "Pop Rock Track"
        song_parameters["theme"] = theme_input.value.strip() or "A beautiful night under neon lights"
        song_parameters["nuance"] = nuance_input.value.strip() or "Energetic and bittersweet"
        
        # Smoothly advance the workspace view forward onto the AI chat workspace room
        nav_callback("Song Generate-AI")

    # Helper function to render a user-friendly labeled form section with descriptive icons
    def create_form_row(icon, title_text, description_text, input_control):
        return ft.Row([
            # Left side: Visual indicator labels describing the field function
            ft.Column([
                ft.Row([
                    ft.Icon(icon, color="#0D6E6E", size=18),
                    ft.Text(title_text, size=14, weight=ft.FontWeight.BOLD, color="#1E293B")
                ], spacing=6),
                ft.Text(description_text, size=11, color="#64748B", width=220)
            ], alignment=ft.MainAxisAlignment.START, spacing=2),
            
            # Right side: The interactive entry element control slot
            input_control
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    # --- WRAPPING THE FORM COMPONENT IN A MODERN CARD VIEW ---
    form_card_container = ft.Container(
        content=ft.Column([
            create_form_row(
                ft.Icons.MUSIC_NOTE_ROUNDED, 
                "Musical Style & Genre", 
                "Select the foundational rhythm template structure for your rhythm pattern.", 
                genre_dropdown
            ),
            ft.Divider(height=24, color="#E2E8F0"),
            create_form_row(
                ft.Icons.LIGHTBULB_OUTLINE_ROUNDED, 
                "Core Concept Theme", 
                "What central narrative timeline ideas or objects should the lyrics center on?", 
                theme_input
            ),
            ft.Divider(height=24, color="#E2E8F0"),
            # FIX: Switched out EMOTIONLESS_ROUNDED for the standard legacy-safe icon PSYCHOLOGY_ROUNDED
            create_form_row(
                ft.Icons.PSYCHOLOGY_ROUNDED, 
                "Atmospheric Nuances", 
                "Specify key sub-genres, tone variables, or signature instrument choices.", 
                nuance_input
            ),
            ft.Divider(height=30, color="transparent"),
            
            # Action button row pushed right
            ft.Row([
                ft.ElevatedButton(
                    "✨ Launch Creative Lyrics Engine", 
                    bgcolor="#0D6E6E", 
                    color="white", 
                    width=280,
                    height=46,
                    on_click=submit_data
                )
            ], alignment=ft.MainAxisAlignment.END)
            
        ], alignment=ft.MainAxisAlignment.START, spacing=10),
        bgcolor="white",
        padding=card_padding,
        border_radius=16,
        width=820,
        border=ft.Border(top=ft.BorderSide(1, "#E2E8F0"), bottom=ft.BorderSide(1, "#E2E8F0"), left=ft.BorderSide(1, "#E2E8F0"), right=ft.BorderSide(1, "#E2E8F0"))
    )

    return ft.Column([
        # Main View Header Titles Group
        ft.Column([
            ft.Text("Configure Lyrics Engine Workspace", size=26, weight=ft.FontWeight.BOLD, color="#1E293B"),
            ft.Text("Set your stylistic boundaries before starting multi-turn generation.", size=14, color="#64748B"),
        ], spacing=2),
        
        ft.Divider(height=20, color="transparent"),
        form_card_container
    ], spacing=10)
