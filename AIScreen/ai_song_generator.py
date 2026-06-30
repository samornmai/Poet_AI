import os
import flet as ft
from google import genai

from Screen.song_generator import song_parameters
from database import save_story_to_db, delete_story_from_db
from session_store import SESSION


def build_song_ai_results_view(nav_callback):
    api_key = os.getenv("GEMINI_API_KEY")
    session_holder = {"client": None, "chat": None}
    is_busy = {"value": False}

    chat_list = ft.ListView(
        expand=True,
        spacing=12,
        auto_scroll=True,
        padding=20,
    )

    def get_or_create_session():
        if session_holder["client"] and session_holder["chat"]:
            return True

        if not api_key:
            return False

        try:
            session_holder["client"] = genai.Client(api_key=api_key)
            system_instruction = (
                f"You are AI Poet. Write songs in {song_parameters.get('genre', 'Pop Rock Track')} style "
                f"about {song_parameters.get('theme', 'hope and connection')} with "
                f"{song_parameters.get('nuance', 'warm and uplifting')} emotion."
            )
            session_holder["chat"] = session_holder["client"].chats.create(
                model="gemini-2.5-flash",
                config={"system_instruction": system_instruction},
            )
            return True
        except Exception as e:
            print("Session error:", e)
            return False

    def ai_bubble(text):
        state = {"saved": False, "id": None}
        current_user_id = SESSION.get("user_id")

        def handle_save(e):
            try:
                if state["saved"]:
                    delete_story_from_db(state["id"])
                    save_btn.icon = ft.Icons.BOOKMARK_BORDER_ROUNDED
                    save_btn.icon_color = "#14B8A6"
                    state["saved"] = False
                    state["id"] = None
                else:
                    words = text.split()
                    title = " ".join(words[:5]) + "..." if len(words) > 5 else text
                    new_id = save_story_to_db(
                        title,
                        text,
                        song_parameters.get("genre", "Lyrics"),
                        "song",
                        current_user_id,
                    )
                    if new_id:
                        state["saved"] = True
                        state["id"] = new_id
                        save_btn.icon = ft.Icons.BOOKMARK_ADDED_ROUNDED
                        save_btn.icon_color = "#0D9488"
            except Exception as ex:
                print("Toggle save error:", ex)
                save_btn.icon = ft.Icons.ERROR_OUTLINE_ROUNDED
                save_btn.icon_color = "red"
            e.page.update()

        save_btn = ft.IconButton(
            icon=ft.Icons.BOOKMARK_BORDER_ROUNDED,
            icon_color="#14B8A6",
            tooltip="Save / Unsave",
            on_click=handle_save,
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.CircleAvatar(content=ft.Text("🤖"), bgcolor="#14B8A6"),
                    ft.SelectionArea(
                        content=ft.Container(
                            content=ft.Text(text, selectable=True, color="#0F172A", size=13),
                            bgcolor="#ECFEFF",
                            padding=15,
                            border_radius=15,
                            width=430,
                            border=ft.border.Border(left=ft.border.BorderSide(3, "#14B8A6")),
                        )
                    ),
                    save_btn,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=4,
            animate=ft.Animation(300, curve=ft.AnimationCurve.DECELERATE),
        )

    def user_bubble(text):
        return ft.Container(
            content=ft.Row(
                [
                    ft.SelectionArea(
                        content=ft.Container(
                            content=ft.Text(text, color="white", selectable=True, size=13),
                            bgcolor="#2563EB",
                            padding=15,
                            border_radius=15,
                            width=430,
                        )
                    ),
                    ft.CircleAvatar(content=ft.Text("👤"), bgcolor="#E2E8F0"),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,
            ),
            padding=4,
            animate=ft.Animation(300, curve=ft.AnimationCurve.DECELERATE),
        )

    def loading_bubble():
        return ft.Container(
            content=ft.Row(
                [
                    ft.ProgressRing(width=18, height=18, stroke_width=2, color="#14B8A6"),
                    ft.Text("Thinking and composing...", color="#64748B", size=12),
                ],
                spacing=10,
            ),
            padding=8,
        )

    user_input = ft.TextField(
        hint_text="Ask AI to improve lyrics...",
        expand=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#F1F5F9",
        border_radius=30,
        content_padding=18,
    )
    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color="white",
        bgcolor="#14B8A6",
    )

    def send_message(e):
        text = user_input.value.strip()
        if not text or is_busy["value"]:
            return

        chat_list.controls.append(user_bubble(text))
        user_input.value = ""
        is_busy["value"] = True
        send_button.disabled = True
        user_input.disabled = True
        loading_row = loading_bubble()
        chat_list.controls.append(loading_row)
        e.page.update()

        if not get_or_create_session():
            if loading_row in chat_list.controls:
                chat_list.controls.remove(loading_row)
            chat_list.controls.append(ai_bubble("Please add your GEMINI_API_KEY to unlock AI generation."))
            is_busy["value"] = False
            send_button.disabled = False
            user_input.disabled = False
            e.page.update()
            return

        try:
            response = session_holder["chat"].send_message(text)
            if loading_row in chat_list.controls:
                chat_list.controls.remove(loading_row)
            chat_list.controls.append(ai_bubble(response.text or "The AI did not return any content yet."))
        except Exception as ex:
            if loading_row in chat_list.controls:
                chat_list.controls.remove(loading_row)
            chat_list.controls.append(ai_bubble(f"Something went wrong: {ex}"))

        is_busy["value"] = False
        send_button.disabled = False
        user_input.disabled = False
        e.page.update()

    user_input.on_submit = send_message
    send_button.on_click = send_message

    chat_list.controls.append(
        ai_bubble(
            f"Hello! I’m ready to write your {song_parameters.get('genre', 'Pop Rock Track')} song about '{song_parameters.get('theme', 'hope and connection')}'. 🎵"
        )
    )

    return ft.Container(
        expand=True,
        bgcolor="#F8FAFC",
        padding=20,
        content=ft.Column(
            [
                ft.Container(
                    bgcolor="#0F172A",
                    padding=20,
                    border_radius=18,
                    shadow=ft.BoxShadow(blur_radius=24, color="#00000020", offset=ft.Offset(0, 8)),
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("🎵 AI Poet", size=26, weight="bold", color="white"),
                                    ft.Text("Your calm, creative songwriting assistant", color="#CBD5E1", size=13),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(icon=ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color="red", tooltip="Clear chat"),
                                    ft.ElevatedButton(
                                        "Reset",
                                        icon=ft.Icons.RESTART_ALT,
                                        bgcolor="#334155",
                                        color="white",
                                        on_click=lambda _: nav_callback("Song Generate"),
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                ft.Container(
                    content=chat_list,
                    bgcolor="white",
                    border_radius=20,
                    expand=True,
                    padding=10,
                    shadow=ft.BoxShadow(blur_radius=20, color="#00000010", offset=ft.Offset(0, 4)),
                ),
                ft.Container(
                    padding=10,
                    content=ft.Row(
                        [
                            user_input,
                            send_button,
                        ]
                    ),
                ),
            ]
        ),
    )