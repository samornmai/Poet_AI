import flet as ft

def create_song_modal(submit_callback, close_callback):
    song_genre = ft.Dropdown(
        label="Genre",
        options=[
            ft.dropdown.Option("Pop"), ft.dropdown.Option("Rock"),
            ft.dropdown.Option("Rap / Hip-Hop"), ft.dropdown.Option("Country"),
            ft.dropdown.Option("Indie / Folk"),
        ],
        border_color="#ffb74d"
    )
    song_mood = ft.TextField(label="Mood (e.g. Melancholic, Energetic)", border_color="#ffb74d")
    song_theme = ft.TextField(label="What is the song about?", multiline=True, min_lines=2, border_color="#ffb74d")

    # This wrapper function extracts the .value from the controls
    def on_submit_click(e):
        submit_callback(song_genre.value, song_mood.value, song_theme.value)
        close_callback(e)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("🎵 Design Your Song Blueprint"),
        content=ft.Column([song_genre, song_mood, song_theme], tight=True, spacing=15),
        actions=[
            ft.TextButton("Cancel", on_click=close_callback, style=ft.ButtonStyle(color="#ffffff")),
            ft.ElevatedButton("Generate Song ✨", on_click=on_submit_click, 
                              style=ft.ButtonStyle(bgcolor="#ffb74d", color="#11111b")),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dialog

def create_story_modal(submit_callback, close_callback):
    story_genre = ft.Dropdown(
        label="Story Genre",
        options=[
            ft.dropdown.Option("Fantasy"), ft.dropdown.Option("Sci-Fi"),
            ft.dropdown.Option("Mystery"), ft.dropdown.Option("Drama"),
            ft.dropdown.Option("Adventure"),
        ],
        border_color="#81c784"
    )
    story_character = ft.TextField(label="Protagonist", border_color="#81c784")
    story_plot = ft.TextField(label="What happens in the plot?", multiline=True, min_lines=2, border_color="#81c784")

    # This wrapper function extracts the .value from the controls
    def on_submit_click(e):
        submit_callback(story_genre.value, story_character.value, story_plot.value)
        close_callback(e)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("📚 Outline Your Short Story"),
        content=ft.Column([story_genre, story_character, story_plot], tight=True, spacing=15),
        actions=[
            ft.TextButton("Cancel", on_click=close_callback, style=ft.ButtonStyle(color="#ffffff")),
            ft.ElevatedButton("Generate Story ✨", on_click=on_submit_click, 
                              style=ft.ButtonStyle(bgcolor="#81c784", color="#11111b")),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    return dialog