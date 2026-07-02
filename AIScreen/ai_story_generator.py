import os
import flet as ft
import google.genai as genai
from Screen.story_generator import story_parameters
from database import save_story_to_db, delete_story_from_db
from session_store import SESSION

RAW_TYPE = "story"


def build_story_ai_results_view(nav_callback):
    api_key = os.getenv("GEMINI_API_KEY")
    session = {"client": None, "chat": None}
    is_busy = {"value": False}

    initial_genre = story_parameters.get("genre", "Cyberpunk Sci-Fi")
    archetype_state = {"value": initial_genre}

    chat = ft.ListView(expand=True, spacing=12, auto_scroll=True, padding=20)

    def get_session():
        if session["client"] and session["chat"]:
            return True
        if not api_key:
            return False
        try:
            session["client"] = genai.Client(api_key=api_key)
            session["chat"] = session["client"].chats.create(
                model="gemini-2.5-flash",
                config={"system_instruction": f"Archetype: {archetype_state['value']}"},
            )
            return True
        except Exception as e:
            print("Session Error:", e)
            return False

    def ai(text):
        is_saved = {"status": False, "id": None}

        def handle_save(e):
            nonlocal is_saved
            current_user_id = SESSION.get("user_id")

            if is_saved["status"]:
                if delete_story_from_db(is_saved["id"]):
                    save_btn.icon = ft.Icons.BOOKMARK_BORDER_ROUNDED
                    save_btn.icon_color = "#14B8A6"
                    is_saved["status"] = False
                    is_saved["id"] = None
            else:
                words = text.split()
                default_title = " ".join(words[:4]) + "..." if len(words) > 4 else text
                new_id = save_story_to_db(
                    default_title,
                    text,
                    archetype_state["value"],
                    RAW_TYPE,
                    current_user_id,
                )
                if new_id:
                    is_saved["status"] = True
                    is_saved["id"] = new_id
                    save_btn.icon = ft.Icons.BOOKMARK_ADDED_ROUNDED
                    save_btn.icon_color = "#0D9488"

            e.page.update()

        save_btn = ft.IconButton(
            icon=ft.Icons.BOOKMARK_BORDER_ROUNDED,
            icon_color="#14B8A6",
            on_click=handle_save,
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.CircleAvatar(content=ft.Text("🤖"), bgcolor="#14B8A6"),
                    ft.SelectionArea(
                        content=ft.Container(
                            content=ft.Text(text, selectable=True, size=13, color="#0F172A"),
                            bgcolor="#ECFEFF",
                            padding=15,
                            border_radius=15,
                            width=430,
                            border=ft.border.Border(left=ft.border.BorderSide(3, "#14B8A6")),
                        )
                    ),
                    save_btn,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=4,
            animate=ft.Animation(300, curve=ft.AnimationCurve.DECELERATE),
        )

    def loading_bubble():
        return ft.Container(
            content=ft.Row(
                [
                    ft.ProgressRing(width=18, height=18, stroke_width=2),
                    ft.Text("Drafting your story...", color="#64748B", size=12),
                ],
                spacing=10,
            ),
            padding=8,
        )

    initial_premise = story_parameters.get("premise") or "A mysterious story..."
    chat.controls.append(ai(f"Start your {archetype_state['value']} story:\n\n{initial_premise}"))

    input_box = ft.TextField(
        hint_text="Continue the story...",
        expand=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#F1F5F9",
        border_radius=30,
        content_padding=18,
    )
    send_button = ft.IconButton(ft.Icons.SEND_ROUNDED, bgcolor="#14B8A6", icon_color="white")

    def send(e):
        message = input_box.value.strip()
        if not message or is_busy["value"]:
            return

        chat.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.SelectionArea(
                            content=ft.Container(
                                content=ft.Text(message, color="white", selectable=True, size=13),
                                bgcolor="#2563EB",
                                padding=15,
                                border_radius=15,
                                width=430,
                            )
                        ),
                        ft.CircleAvatar(content=ft.Text("👤"), bgcolor="#E2E8F0"),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=4,
            )
        )
        input_box.value = ""
        is_busy["value"] = True
        send_button.disabled = True
        input_box.disabled = True
        chat.controls.append(loading_bubble())
        e.page.update()

        if not get_session():
            chat.controls[-1] = ai("Please add your GEMINI_API_KEY to unlock AI generation.")
            is_busy["value"] = False
            send_button.disabled = False
            input_box.disabled = False
            e.page.update()
            return

        try:
            response = session["chat"].send_message(message)
            chat.controls.pop()
            chat.controls.append(ai(response.text or "The AI did not return any content yet."))
        except Exception as ex:
            chat.controls.pop()
            chat.controls.append(ai(f"Something went wrong: {ex}"))

        is_busy["value"] = False
        send_button.disabled = False
        input_box.disabled = False
        e.page.update()

    input_box.on_submit = send
    send_button.on_click = send

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
                            ft.Column([ft.Text("📖 AI Storyteller", size=26, weight="bold", color="white")]),
                            ft.Row(
                                [
                                    ft.IconButton(ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color="red", tooltip="Clear chat"),
                                    ft.ElevatedButton("Settings", on_click=lambda _: nav_callback("Generate Story"), bgcolor="#334155", color="white"),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                ft.Container(
                    content=chat,
                    bgcolor="white",
                    border_radius=20,
                    expand=True,
                    padding=10,
                    shadow=ft.BoxShadow(blur_radius=20, color="#00000010", offset=ft.Offset(0, 4)),
                ),
                ft.Container(
                    padding=10,
                    content=ft.Row([input_box, send_button]),
                ),
            ]
        ),
    )