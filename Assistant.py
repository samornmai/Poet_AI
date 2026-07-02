import flet as ft
import google.genai as genai
import os
from database import save_story_to_db


CURRENT_USER = 1


# ---------------- GLOBAL STATE ----------------
chat_history_controls = ft.ListView(
    expand=True,
    spacing=12,
    auto_scroll=True,
    padding=20,
    scroll=ft.ScrollMode.HIDDEN,
)

session = {"client": None, "chat": None}


# ---------------- GEMINI SESSION ----------------
def get_session():
    if session["client"] and session["chat"]:
        return True

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Missing GEMINI_API_KEY in .env file")
        return False

    try:
        # Initialize Gemini API with direct client creation (consistent with other modules)
        session["client"] = genai.Client(api_key=api_key)

        session["chat"] = session["client"].chats.create(
            model="gemini-2.5-flash",
            config={
                "system_instruction": "You are a helpful AI assistant for creative writing. Help users with songwriting, storytelling, and creative ideas."
            },
        )

        print("✅ Gemini API session initialized successfully")
        return True

    except Exception as e:
        print(f"❌ Session error: {str(e)}")
        print(f"API Key loaded: {bool(api_key)}")
        print(f"API Key format: {api_key[:20] if api_key else 'None'}...")
        return False



# ---------------- SAVE FUNCTION ----------------
def save_to_db(text, category):
    words = text.split()
    title = " ".join(words[:5]) + "..." if len(words) > 5 else text

    save_story_to_db(
        title=title,
        content=text,
        genre=category,
        save_type=category.lower(),  # story or song
        user_id=CURRENT_USER,
    )


# ---------------- MAIN VIEW (IMPORTANT NAME FIX) ----------------
def build_chat_assistant_view(nav_callback):

    # -------- CLEAR CHAT --------
    def clear_chat_history(e):
        def clear(ev):
            chat_history_controls.controls.clear()
            session["chat"] = None
            ev.page.dialog.open = False
            ev.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Clear Chat?"),
            content=ft.Text("Delete all messages?"),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=lambda ev: (
                        setattr(ev.page.dialog, "open", False),
                        ev.page.update(),
                    ),
                ),
                ft.TextButton("Clear", on_click=clear, style=ft.ButtonStyle(color="red")),
            ],
        )

        e.page.dialog = dlg
        dlg.open = True
        e.page.update()

    # -------- AI MESSAGE --------
    def ai_message(text):

        save_btn = ft.IconButton(
            icon=ft.Icons.BOOKMARK_BORDER_ROUNDED,
            icon_color="#14B8A6",
        )

        def open_save_dialog(e):

            def choose(ev):
                category = ev.control.text  # Story / Song

                save_to_db(text, category)

                save_btn.icon = ft.Icons.BOOKMARK_ADDED_ROUNDED
                save_btn.icon_color = "#0D9488"

                ev.page.dialog.open = False
                ev.page.update()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Save as:"),
                content=ft.Column(
                    [
                        ft.ElevatedButton("Story", on_click=choose, bgcolor="#14B8A6", color="white"),
                        ft.ElevatedButton("Song", on_click=choose, bgcolor="#2563EB", color="white"),
                    ],
                    tight=True,
                    height=120,
                ),
                actions=[
                    ft.TextButton(
                        "Cancel",
                        on_click=lambda ev: (
                            setattr(ev.page.dialog, "open", False),
                            ev.page.update(),
                        ),
                    )
                ],
            )

            e.page.dialog = dlg
            dlg.open = True
            e.page.update()

        save_btn.on_click = open_save_dialog

        return ft.Row(
            [
                ft.CircleAvatar(content=ft.Text("🤖"), bgcolor="#14B8A6"),
                ft.SelectionArea(
                    content=ft.Container(
                        content=ft.Text(text, selectable=True),
                        bgcolor="#ECFEFF",
                        padding=15,
                        border_radius=15,
                        width=450,
                    )
                ),
                save_btn,
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    # -------- USER MESSAGE --------
    def user_message(text):
        return ft.Row(
            [
                ft.SelectionArea(
                    content=ft.Container(
                        content=ft.Text(text, color="white"),
                        bgcolor="#2563EB",
                        padding=15,
                        border_radius=15,
                        width=500,
                    )
                ),
                ft.CircleAvatar(content=ft.Text("👤")),
            ],
            alignment=ft.MainAxisAlignment.END,
        )

    # -------- INPUT --------
    input_box = ft.TextField(
        hint_text="Ask me anything...",
        expand=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor="#F1F5F9",
        border_radius=30,
        content_padding=18,
    )

    def send(e):
        text = input_box.value.strip()
        if not text:
            return

        chat_history_controls.controls.append(user_message(text))
        input_box.value = ""

        loading = ft.Text("Thinking...", italic=True, color="#64748B")
        chat_history_controls.controls.append(loading)
        e.page.update()

        if get_session():
            try:
                res = session["chat"].send_message(text)
                chat_history_controls.controls.remove(loading)
                chat_history_controls.controls.append(ai_message(res.text))
            except Exception as err:
                chat_history_controls.controls.remove(loading)
                chat_history_controls.controls.append(ai_message(f"Error: {err}"))
        else:
            chat_history_controls.controls.remove(loading)
            chat_history_controls.controls.append(
                ai_message("Error: connection failed.")
            )

        e.page.update()

    input_box.on_submit = send

    # -------- UI --------
    return ft.Container(
        expand=True,
        bgcolor="#F8FAFC",
        padding=20,
        content=ft.Column(
            [
                ft.Container(
                    bgcolor="#0F172A",
                    padding=20,
                    border_radius=15,
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("💬 Chat Assistant", size=26, weight="bold", color="white"),
                                    ft.Text("Your AI companion", color="#CBD5E1", size=13),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                        icon_color="red",
                                        tooltip="Clear Chat",
                                        on_click=clear_chat_history,
                                    ),
                                    ft.ElevatedButton(
                                        "Back",
                                        bgcolor="#334155",
                                        color="white",
                                        on_click=lambda _: nav_callback("Dashboard"),
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                ft.Container(
                    content=chat_history_controls,
                    bgcolor="white",
                    border_radius=20,
                    expand=True,
                    padding=10,
                ),
                ft.Container(
                    padding=10,
                    content=ft.Row(
                        [
                            input_box,
                            ft.IconButton(
                                icon=ft.Icons.SEND_ROUNDED,
                                bgcolor="#14B8A6",
                                icon_color="white",
                                on_click=send,
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )