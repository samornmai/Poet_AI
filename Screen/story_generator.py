import flet as ft

# Global memory to hold selections safely across screen refreshes
story_parameters = {"genre": "", "premise": ""}

def build_story_generate_view(nav_callback):
    # Safe legacy padding initialization
    card_padding = ft.padding.Padding(left=28, top=28, right=28, bottom=28)
    
    # --- FORM INPUT CONTROLS CONFIGURATION ---
    genre_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Cyberpunk Sci-Fi"), 
            ft.dropdown.Option("High Fantasy Quest"), 
            ft.dropdown.Option("Noir Mystery Script"),
            ft.dropdown.Option("Psychological Thriller"),
            ft.dropdown.Option("Historical Drama")
        ],
        hint_text="Choose a literary archetype...",
        width=500, 
        bgcolor="#F8FAFC", 
        border_radius=8,
        border_color="#CBD5E1"
    )
    
    premise_input = ft.TextField(
        hint_text="Provide initial character backgrounds, settings, conflict lines, or narrative plot twists...", 
        multiline=True, 
        min_lines=4, 
        max_lines=6, 
        width=500, 
        bgcolor="#F8FAFC",
        border_radius=8,
        border_color="#CBD5E1",
        content_padding=12
    )

    # --- ACTION SUBMIT ROUTING CONTEXT ---
    def submit_data(e):
        # Fallback safe defaults if user leaves field slots empty
        story_parameters["genre"] = genre_dropdown.value or "Cyberpunk Sci-Fi"
        story_parameters["premise"] = premise_input.value.strip() or "A rogue AI breaks containment in a corporate city"
        
        # Smoothly advance the workspace view forward onto the AI chat workspace room
        nav_callback("Generate Story AI")

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
                ft.Icons.AUTO_STORIES_ROUNDED, 
                "Literary Archetype", 
                "Select the primary world-building genre foundation for your novel.", 
                genre_dropdown
            ),
            ft.Divider(height=24, color="#E2E8F0"),
            create_form_row(
                ft.Icons.LIGHTBULB_OUTLINE_ROUNDED, 
                "Plot Outline Premise", 
                "Outline your initial characters, settings, motivations, or thematic conflicts.", 
                premise_input
            ),
            ft.Divider(height=30, color="transparent"),
            
            # Action button row pushed right
            ft.Row([
                ft.ElevatedButton(
                    "✨ Launch Creative Story Engine", 
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
            ft.Text("Configure Story Scriptorium", size=26, weight=ft.FontWeight.BOLD, color="#1E293B"),
            ft.Text("Set your conceptual premise boundaries before writing your chapters.", size=14, color="#64748B"),
        ], spacing=2),
        
        ft.Divider(height=20, color="transparent"),
        form_card_container
    ], spacing=10)
