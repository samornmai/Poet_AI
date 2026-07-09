import os
import random
import sqlite3
import string
import time

import flet as ft

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from dashboard import create_dashboard_view


load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

SYSTEM_PROMPT = (
    "You are Poet AI. Help only with songs, poems, story poems, and creative stories. "
    "If the user asks for anything else, politely say you can help with songs, poems, or story writing only. "
    "Keep replies concise, friendly, and creative."
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            token TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def ensure_default_admin():
    conn = get_connection()
    admin = conn.execute("SELECT id FROM users WHERE username = ?", ("Admin",)).fetchone()
    if admin is None:
        token = f"ADM{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))}"
        conn.execute(
            "INSERT INTO users (username, email, password, token) VALUES (?, ?, ?, ?)",
            ("Admin", "admin@poet.local", "Admin123", token),
        )
        conn.commit()
    conn.close()


def create_user(username, email, password):
    token = f"{username[:3].upper()}{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))}"
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, email, password, token) VALUES (?, ?, ?, ?)",
            (username, email, password, token),
        )
        conn.commit()
    except sqlite3.IntegrityError as exc:
        conn.close()
        raise ValueError("username or email already exists") from exc
    finally:
        conn.close()
    return {"username": username, "email": email, "token": token, "id": cursor.lastrowid}


def verify_login(username, password):
    conn = get_connection()
    row = conn.execute(
        "SELECT username FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()
    return row is not None


def get_user_by_username(username):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, username, email, token FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def list_users():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, username, email, password, token FROM users ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_user(user_id, username, email, password=None):
    conn = get_connection()
    existing = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
    if existing is None:
        conn.close()
        raise ValueError("user not found")
    try:
        if password:
            conn.execute(
                "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
                (username, email, password, user_id),
            )
        else:
            conn.execute(
                "UPDATE users SET username = ?, email = ? WHERE id = ?",
                (username, email, user_id),
            )
        conn.commit()
    except sqlite3.IntegrityError as exc:
        conn.close()
        raise ValueError("username or email already exists") from exc
    finally:
        conn.close()
    return existing["username"]


init_db()
ensure_default_admin()


def main(page: ft.Page):
    page.title = "Poet AI"
    page.padding = 0
    page.bgcolor = "#060816"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 800

    try:
        api_key = os.getenv("GROQ_API_KEY")
        model = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key) if api_key else None
    except Exception:
        model = None

    current_view = "home"
    current_user = None
    auth_message = ""
    admin_message = ""
    user_sessions = {}
    sidebar_open = True

    def build_bubble(text, is_user, is_thinking=False):
        page_width = page.width or page.window_width or 1200
        bubble_width = min(680, int(page_width * 0.58))

        if is_user:
            bubble = ft.Container(
                content=ft.Text(text, selectable=True, color="#FFFFFF", size=14),
                bgcolor="#087879",
                padding=ft.padding.Padding(left=16, top=12, right=16, bottom=12),
                border_radius=ft.BorderRadius(top_left=18, top_right=6, bottom_left=18, bottom_right=18),
                width=bubble_width,
            )
            avatar = ft.Container(
                content=ft.Icon(ft.Icons.PERSON_ROUNDED, size=18, color="#FFFFFF"),
                width=36,
                height=36,
                border_radius=18,
                bgcolor="#0F766E",
                alignment=ft.Alignment(0, 0),
            )
            return ft.Container(
                content=ft.Row(
                    [ft.Container(expand=True), bubble, avatar],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=10,
                ),
                margin=ft.Margin(left=0, top=0, right=0, bottom=14),
            )

        avatar = ft.Container(
            content=ft.ProgressRing(width=18, height=18, stroke_width=2, color="#087879")
            if is_thinking
            else ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, size=19, color="#087879"),
            width=36,
            height=36,
            border_radius=18,
            bgcolor="#E0F7F7",
            alignment=ft.Alignment(0, 0),
        )
        if is_thinking:
            bubble_content = ft.Row(
                [
                    ft.Text("AI is generating...", color="#087879", size=14, weight=ft.FontWeight.W_500),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            bubble_bg = "#E0F7F7"
            bubble_border = "#99D9DA"
        else:
            bubble_content = ft.Text(text, selectable=True, color="#111827", size=14)
            bubble_bg = "#FFFFFF"
            bubble_border = "#E5E7EB"

        bubble = ft.Container(
            content=bubble_content,
            bgcolor=bubble_bg,
            padding=ft.padding.Padding(left=16, top=12, right=16, bottom=12),
            border_radius=ft.BorderRadius(top_left=6, top_right=18, bottom_left=18, bottom_right=18),
            border=ft.Border.all(1, bubble_border),
            width=bubble_width,
        )
        return ft.Container(
            content=ft.Row(
                [avatar, bubble, ft.Container(expand=True)],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=10,
            ),
            margin=ft.Margin(left=0, top=0, right=0, bottom=14),
        )
    def is_supported_request(prompt):
        lowered = prompt.lower()
        keywords = [
            "song",
            "songs",
            "lyric",
            "lyrics",
            "poem",
            "poems",
            "poetry",
            "story",
            "stories",
            "story poem",
            "tale",
            "narrative",
            "chorus",
            "verse",
            "ballad",
            "rhyme",
        ]
        return any(keyword in lowered for keyword in keywords)

    def get_request_kind(prompt):
        lowered = prompt.lower()
        song_keywords = ["song", "songs", "lyric", "lyrics", "chorus", "verse", "ballad"]
        story_keywords = ["story", "stories", "story poem", "tale", "narrative", "character"]

        if any(keyword in lowered for keyword in song_keywords):
            return "song"
        if any(keyword in lowered for keyword in story_keywords):
            return "story"
        return "poem"

    def build_creative_dashboard_stats(user_data):
        sessions = user_data.get("sessions", [])
        stats = {
            "poems": 0,
            "songs": 0,
            "stories": 0,
            "sessions": len(sessions),
            "messages": 0,
            "momentum": 0,
        }

        for session in sessions:
            for message in session.get("messages", []):
                if message.get("thinking"):
                    continue
                stats["messages"] += 1
                if message.get("role") != "user":
                    continue

                text = message.get("text", "")
                if not is_supported_request(text):
                    continue

                request_kind = get_request_kind(text)
                if request_kind == "song":
                    stats["songs"] += 1
                elif request_kind == "story":
                    stats["stories"] += 1
                else:
                    stats["poems"] += 1

        creative_total = stats["poems"] + stats["songs"] + stats["stories"]
        stats["momentum"] = min(100, creative_total * 10)
        return stats

    def generate_ai_response(prompt):
        if model is None:
            return "Poet AI is ready. I can help you write a song, poem, story poem, or story. Try a short prompt like: 'Write a sad pop song about midnight.'"

        try:
            response = model.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ])
            return response.content
        except Exception:
            return "Poet AI is temporarily unavailable. Please try again in a moment."

    def ensure_user_session(user_name):
        if user_name not in user_sessions:
            user_sessions[user_name] = {"sessions": [], "active_session": None}
        return user_sessions[user_name]

    def build_home_view():
        page_width = page.width or page.window_width or 1200
        is_mobile = page_width < 760
        panel_width = page_width
        panel_height = page.height or page.window_height or 800
        side_padding = 42 if not is_mobile else 24
        top_padding = 38 if not is_mobile else 24
        headline_size = 42 if not is_mobile else 34
        headline_width = 430 if not is_mobile else max(panel_width - 48, 260)
        hero_icon_size = 126 if not is_mobile else 86
        hero_circle_size = 214 if not is_mobile else 148

        nav = ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.EDIT_ROUNDED, color="white", size=18),
                        ft.Text("Poet AI", color="white", size=20, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Login",
                            width=110 if not is_mobile else 92,
                            height=38,
                            bgcolor="#00AEB8",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            on_click=lambda e: (set_view("login"), render()),
                        ),
                        ft.ElevatedButton(
                            "Sign Up",
                            width=110 if not is_mobile else 100,
                            height=38,
                            bgcolor="#00AEB8",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            on_click=lambda e: (set_view("signup"), render()),
                        ),
                    ],
                    spacing=12,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        hero_text = ft.Column(
            [
                ft.Text(
                    "Create Stories\nand Song with\nAI Poet",
                    width=headline_width,
                    size=headline_size,
                    color="white",
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.LEFT,
                ),
                ft.Text("Wel com to AI generator", color="white", size=16, weight=ft.FontWeight.W_500),
            ],
            spacing=26,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        hero_icon = ft.Container(
            width=hero_circle_size,
            height=hero_circle_size,
            border_radius=hero_circle_size / 2,
            bgcolor="#178F92",
            opacity=0.85,
            alignment=ft.Alignment(0, 0),
            content=ft.Icon(ft.Icons.HUB_ROUNDED, color="white", size=hero_icon_size),
        )

        hero_content = ft.Row(
            [hero_text, hero_icon],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=is_mobile,
            spacing=32,
        )

        panel = ft.Container(
            width=panel_width,
            height=panel_height,
            padding=ft.padding.Padding(left=side_padding, top=top_padding, right=side_padding, bottom=top_padding),
            border=ft.Border.all(2, "#0B8DFF"),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#078FB2", "#48AAA8"],
            ),
            content=ft.Column(
                [
                    nav,
                    ft.Container(height=28 if not is_mobile else 36),
                    hero_content,
                ],
                spacing=0,
            ),
        )

        return ft.Container(
            expand=True,
            bgcolor="#078FB2",
            padding=0,
            content=panel,
        )
    def build_auth_view(mode):
        page_width = page.width or page.window_width or 1200
        is_mobile = page_width < 760
        card_width = min(page_width - 48, 360) if is_mobile else 360
        field_width = card_width - 58

        def auth_field(label, password=False):
            return ft.TextField(
                label=label,
                password=password,
                width=field_width,
                height=52,
                border_radius=10,
                border_color="#F8F8F8",
                focused_border_color="#00AEB8",
                bgcolor="#FFFFFF",
                color="#0F172A",
                label_style=ft.TextStyle(color="#0F172A", size=11, weight=ft.FontWeight.BOLD),
                text_style=ft.TextStyle(color="#0F172A", size=14),
                cursor_color="#007879",
                content_padding=ft.padding.Padding(left=14, top=8, right=14, bottom=8),
            )

        username_field = auth_field("User Name" if mode == "signup" else "Username")
        password_field = auth_field("Password", password=True)
        confirm_password_field = auth_field("Re-Password", password=True) if mode == "signup" else None
        info_color = "#007879" if auth_message and "Invalid" not in auth_message and "Please" not in auth_message and "already exists" not in auth_message and "match" not in auth_message else "#B42318"
        info_text = ft.Text(auth_message, color=info_color, size=12, text_align=ft.TextAlign.CENTER)

        def handle_submit(e):
            nonlocal current_user, auth_message
            username = username_field.value.strip()
            password = password_field.value.strip()
            if not username or not password:
                auth_message = "Please fill in both fields."
                render()
                return

            if mode == "signup":
                confirm_password = confirm_password_field.value.strip() if confirm_password_field else ""
                if not confirm_password:
                    auth_message = "Please confirm your password."
                    render()
                    return
                if password != confirm_password:
                    auth_message = "Passwords do not match."
                    render()
                    return
                email = f"{username.lower()}@poet.local"
                try:
                    user = create_user(username, email, password)
                except ValueError:
                    auth_message = "That username already exists."
                    render()
                    return
                auth_message = f"Account created. Your token: {user['token']}"
                current_user = username
                set_view("dashboard")
                render()
                return

            if verify_login(username, password):
                auth_message = "Welcome back!"
                current_user = username
                set_view("dashboard")
                render()
            else:
                auth_message = "Invalid username or password."
                render()

        title = "Sign up" if mode == "signup" else "Login"
        switch_label = "Sign in" if mode == "signup" else "Sign Up"
        switch_target = "login" if mode == "signup" else "signup"

        nav = ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.EDIT_ROUNDED, color="white", size=18),
                        ft.Text("Poet AI", color="white", size=20, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.ElevatedButton(
                    switch_label,
                    width=112,
                    height=38,
                    bgcolor="#00AEB8",
                    color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=lambda e: (set_view(switch_target), render()),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        headline = ft.Text(
            "Create Stories\nand Song with\nAI Poet",
            width=430 if not is_mobile else card_width,
            size=36 if is_mobile else 42,
            color="white",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.LEFT,
        )

        fields = [username_field, password_field]
        if confirm_password_field is not None:
            fields.append(confirm_password_field)

        auth_card = ft.Container(
            width=card_width,
            padding=ft.padding.Padding(left=26, top=16, right=26, bottom=24),
            border_radius=8,
            bgcolor="#D9F6F8",
            content=ft.Column(
                [
                    ft.Text(title, color="#0F172A", size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    *fields,
                    ft.Container(height=8),
                    ft.ElevatedButton(
                        title,
                        on_click=handle_submit,
                        width=field_width,
                        height=44,
                        bgcolor="#00AEB8",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    ),
                    info_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        )

        body = ft.Row(
            [headline, auth_card],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=is_mobile,
            spacing=42,
        )

        return ft.Container(
            expand=True,
            bgcolor="#087879",
            padding=ft.padding.Padding(left=32, top=34, right=32, bottom=34),
            content=ft.Column(
                [
                    nav,
                    ft.Container(height=48 if not is_mobile else 28),
                    body,
                ],
                spacing=0,
            ),
        )
    def build_dashboard_view():
        user_data = ensure_user_session(current_user)
        sessions = user_data.get("sessions", [])
        active_session = user_data.get("active_session")
        chat_history = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=12)

        def creator_text_field(label, hint="", multiline=False):
            return ft.TextField(
                label=label,
                hint_text=hint,
                multiline=multiline,
                min_lines=3 if multiline else 1,
                max_lines=5 if multiline else 1,
                border_radius=10,
                border_color="#CDEDEE",
                focused_border_color="#087879",
                bgcolor="#FFFFFF",
                color="#111827",
                cursor_color="#087879",
                label_style=ft.TextStyle(color="#0F172A", size=12, weight=ft.FontWeight.BOLD),
                hint_style=ft.TextStyle(color="#94A3B8", size=13),
                text_style=ft.TextStyle(color="#111827", size=14),
                content_padding=ft.padding.Padding(left=14, top=12, right=14, bottom=12),
            )

        def creator_dropdown(label, options, value):
            return ft.Dropdown(
                label=label,
                value=value,
                options=[ft.dropdown.Option(option) for option in options],
                border_radius=10,
                border_color="#CDEDEE",
                focused_border_color="#087879",
                bgcolor="#FFFFFF",
                color="#111827",
                label_style=ft.TextStyle(color="#0F172A", size=12, weight=ft.FontWeight.BOLD),
                text_style=ft.TextStyle(color="#111827", size=14),
            )

        def creator_dialog_title(icon, title, subtitle):
            return ft.Row(
                [
                    ft.Container(
                        width=38,
                        height=38,
                        border_radius=19,
                        bgcolor="#E0F7F7",
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon, color="#087879", size=21),
                    ),
                    ft.Column(
                        [
                            ft.Text(title, color="#0F172A", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(subtitle, color="#64748B", size=12),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

        if not hasattr(page, "song_dialog"):
            page.song_genre = creator_dropdown("Genre", ["Pop", "Rock", "Rap / Hip-Hop", "Country", "Indie / Folk", "R&B", "Ballad"], "Pop")
            page.song_mood = creator_text_field("Mood", "Energetic, sad, romantic, hopeful...")
            page.song_topic = creator_text_field("Song topic", "What should the song be about?", multiline=True)
            page.song_style = creator_text_field("Extra direction", "Optional: language, artist vibe, chorus focus...")
            page.song_dialog = ft.AlertDialog(
                modal=True,
                bgcolor="#F8FFFF",
                title=creator_dialog_title(ft.Icons.MUSIC_NOTE_ROUNDED, "Song Creator", "Build a polished lyric prompt"),
                content=ft.Container(
                    width=430,
                    content=ft.Column(
                        [page.song_genre, page.song_mood, page.song_topic, page.song_style],
                        tight=True,
                        spacing=12,
                    ),
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda e: None, style=ft.ButtonStyle(color="#64748B")),
                    ft.ElevatedButton(
                        "Generate Song",
                        on_click=lambda e: None,
                        bgcolor="#087879",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.overlay.append(page.song_dialog)

        if not hasattr(page, "story_dialog"):
            page.story_genre = creator_dropdown("Genre", ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Drama", "Romance", "Horror"], "Fantasy")
            page.story_character = creator_text_field("Main character", "Name, role, or personality")
            page.story_plot = creator_text_field("Story idea", "What happens in the story?", multiline=True)
            page.story_tone = creator_text_field("Tone and ending", "Optional: warm, dark, funny, twist ending...")
            page.story_dialog = ft.AlertDialog(
                modal=True,
                bgcolor="#F8FFFF",
                title=creator_dialog_title(ft.Icons.MENU_BOOK_ROUNDED, "Story Creator", "Turn an idea into a complete scene"),
                content=ft.Container(
                    width=430,
                    content=ft.Column(
                        [page.story_genre, page.story_character, page.story_plot, page.story_tone],
                        tight=True,
                        spacing=12,
                    ),
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda e: None, style=ft.ButtonStyle(color="#64748B")),
                    ft.ElevatedButton(
                        "Generate Story",
                        on_click=lambda e: None,
                        bgcolor="#087879",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.overlay.append(page.story_dialog)
        if active_session:
            selected = next((s for s in sessions if s["title"] == active_session), None)
            if selected:
                for message in selected.get("messages", []):
                    chat_history.controls.append(build_bubble(message["text"], message["role"] == "user", message.get("thinking", False)))
        else:
            chat_history.controls.append(build_bubble("Hello! I can help with songs, poems, story poems, and stories. Ask me for a lyric, poem, or story idea.", is_user=False))

        user_input = ft.TextField(
            hint_text="Message Poet AI...",
            expand=True,
            border_radius=16,
            border_color="#D1D5DB",
            focused_border_color="#087879",
            cursor_color="#087879",
            content_padding=ft.padding.Padding(left=16, top=14, right=16, bottom=14),
            bgcolor="#FFFFFF",
            color="#111827",
            text_style=ft.TextStyle(color="#111827", size=14),
            hint_style=ft.TextStyle(color="#6B7280", size=14),
            multiline=True,
            min_lines=1,
            max_lines=4,
        )

        def save_message(text, role, thinking=False):
            nonlocal active_session
            if not active_session:
                title = text[:30]
                count = 1
                original = title
                while any(s["title"] == title for s in sessions):
                    title = f"{original} {count}"
                    count += 1
                sessions.append({"title": title, "messages": []})
                user_data["active_session"] = title
                active_session = title
            selected = next((s for s in sessions if s["title"] == user_data["active_session"]), None)
            if selected is not None:
                selected["messages"].append({"text": text, "role": role, "thinking": thinking})

        def replace_last_thinking_message(answer):
            selected = next((s for s in sessions if s["title"] == user_data["active_session"]), None)
            if selected and selected["messages"]:
                selected["messages"][-1] = {"text": answer, "role": "ai", "thinking": False}

        def generate_with_delay(prompt):
            save_message("AI is thinking...", "ai", thinking=True)
            render()
            time.sleep(5)
            answer = generate_ai_response(prompt)
            replace_last_thinking_message(answer)
            render()

        def clean_creator_prefill(text, kind):
            lowered = text.lower().strip(" .!?")
            generic_requests = {
                "song",
                "write song",
                "create song",
                "make song",
                "generate song",
                "story",
                "write story",
                "create story",
                "make story",
                "generate story",
            }
            return "" if lowered in generic_requests else text

        def open_creator_from_chat(text, kind):
            user_data["pending_creator"] = kind
            if kind == "song":
                if not (page.song_topic.value or "").strip():
                    page.song_topic.value = clean_creator_prefill(text, kind)
                page.song_topic.error_text = None
                page.song_dialog.open = True
                save_message("Sure. Fill in the Song Creator form, then click Generate Song.", "ai")
            else:
                if not (page.story_plot.value or "").strip():
                    page.story_plot.value = clean_creator_prefill(text, kind)
                page.story_plot.error_text = None
                page.story_dialog.open = True
                save_message("Sure. Fill in the Story Creator form, then click Generate Story.", "ai")
            render()
            if kind == "song":
                page.song_dialog.open = True
            else:
                page.story_dialog.open = True
            page.update()

        def send_message(e):
            text = user_input.value.strip()
            if not text:
                return
            save_message(text, "user")
            user_input.value = ""
            render()
            if not is_supported_request(text):
                save_message("I can only help with songs, poems, story poems, or stories. Try asking me to write a song, poem, or creative story.", "ai")
                render()
                return
            request_kind = get_request_kind(text)
            if request_kind in ("song", "story"):
                open_creator_from_chat(text, request_kind)
                return
            generate_with_delay(text)

        user_input.on_submit = send_message

        def load_session(e, session_title):
            user_data["active_session"] = session_title
            render()

        def new_chat(e):
            user_data["active_session"] = None
            user_data["pending_creator"] = None
            reset_creator_dialogs()
            set_view("chat")
            render()

        def logout(e):
            nonlocal current_user, auth_message
            current_user = None
            auth_message = ""
            set_view("home")
            render()

        def open_song_dialog(e):
            page.song_dialog.open = True
            page.update()

        def reopen_pending_creator(e):
            pending_creator = user_data.get("pending_creator")
            if pending_creator == "song":
                page.song_dialog.open = True
            elif pending_creator == "story":
                page.story_dialog.open = True
            page.update()

        def reset_creator_dialogs():
            if hasattr(page, "song_genre"):
                page.song_genre.value = "Pop"
                page.song_mood.value = ""
                page.song_topic.value = ""
                page.song_topic.error_text = None
                page.song_style.value = ""
            if hasattr(page, "story_genre"):
                page.story_genre.value = "Fantasy"
                page.story_character.value = ""
                page.story_plot.value = ""
                page.story_plot.error_text = None
                page.story_tone.value = ""

        def create_song_from_dialog(e):
            genre = (page.song_genre.value or "Pop").strip()
            mood = (page.song_mood.value or "").strip()
            topic = (page.song_topic.value or "").strip()
            style = (page.song_style.value or "").strip()

            page.song_topic.error_text = None

            prompt_parts = [
                "Create a complete song with title, verses, chorus, bridge, and a short creative note.",
                f"Genre: {genre}.",
                f"Topic: {topic}." if topic else "Topic: choose an original theme that fits the selected genre.",
            ]
            if mood:
                prompt_parts.append(f"Mood: {mood}.")
            if style:
                prompt_parts.append(f"Extra direction: {style}.")
            prompt = " ".join(prompt_parts)

            user_data["pending_creator"] = None
            page.song_dialog.open = False
            set_view("chat")
            page.update()
            save_message(prompt, "user")
            render()
            generate_with_delay(prompt)
        def open_story_dialog(e):
            page.story_dialog.open = True
            page.update()

        def create_story_from_dialog(e):
            genre = (page.story_genre.value or "Fantasy").strip()
            character = (page.story_character.value or "").strip()
            plot = (page.story_plot.value or "").strip()
            tone = (page.story_tone.value or "").strip()

            page.story_plot.error_text = None

            prompt_parts = [
                "Create a polished short story with a title, vivid opening, clear conflict, satisfying ending, and a brief theme note.",
                f"Genre: {genre}.",
                f"Story idea: {plot}." if plot else "Story idea: choose an original premise that fits the selected genre.",
            ]
            if character:
                prompt_parts.append(f"Main character: {character}.")
            if tone:
                prompt_parts.append(f"Tone and ending: {tone}.")
            prompt = " ".join(prompt_parts)

            user_data["pending_creator"] = None
            page.story_dialog.open = False
            set_view("chat")
            page.update()
            save_message(prompt, "user")
            render()
            generate_with_delay(prompt)
        page.song_dialog.actions[1].on_click = create_song_from_dialog
        page.story_dialog.actions[1].on_click = create_story_from_dialog
        page.song_dialog.actions[0].on_click = lambda e: (setattr(page.song_dialog, "open", False), page.update())
        page.story_dialog.actions[0].on_click = lambda e: (setattr(page.story_dialog, "open", False), page.update())

        user_info = get_user_by_username(current_user) or {}

        def toggle_sidebar(e):
            nonlocal sidebar_open
            sidebar_open = not sidebar_open
            render()

        def toggle_theme(e):
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode = ft.ThemeMode.LIGHT
                page.bgcolor = "#F7FAFA"
            else:
                page.theme_mode = ft.ThemeMode.DARK
                page.bgcolor = "#060816"
            render()

        def build_admin_users_view():
            all_users = list_users()
            status_color = "#16A34A" if admin_message.startswith("Saved") else "#DC2626"

            def admin_field(value="", hint="", password=False, width=170):
                return ft.TextField(
                    value=value,
                    hint_text=hint,
                    password=password,
                    width=width,
                    height=44,
                    border_radius=8,
                    border_color="#D1D5DB",
                    focused_border_color="#087879",
                    bgcolor="#FFFFFF",
                    color="#111827",
                    text_style=ft.TextStyle(color="#111827", size=13),
                    hint_style=ft.TextStyle(color="#94A3B8", size=12),
                    content_padding=ft.padding.Padding(left=10, top=8, right=10, bottom=8),
                )

            def build_user_row(user):
                username_field = admin_field(user["username"], width=150)
                email_field = admin_field(user["email"], width=210)
                password_field = admin_field("", "new password", password=True, width=150)
                session_count = len(user_sessions.get(user["username"], {}).get("sessions", []))

                def save_user(e):
                    nonlocal current_user, admin_message
                    new_username = username_field.value.strip()
                    new_email = email_field.value.strip()
                    new_password = password_field.value.strip()
                    if not new_username or not new_email:
                        admin_message = "Username and email are required."
                        render()
                        return
                    try:
                        old_username = update_user(user["id"], new_username, new_email, new_password or None)
                    except ValueError as exc:
                        admin_message = str(exc).capitalize()
                        render()
                        return
                    if old_username != new_username and old_username in user_sessions:
                        user_sessions[new_username] = user_sessions.pop(old_username)
                    if current_user == old_username:
                        current_user = new_username
                    admin_message = f"Saved {new_username}."
                    render()

                return ft.Container(
                    bgcolor="#FFFFFF",
                    border=ft.Border.all(1, "#E5E7EB"),
                    border_radius=8,
                    padding=ft.padding.Padding(left=12, top=10, right=12, bottom=10),
                    content=ft.Row(
                        [
                            ft.Text(str(user["id"]), width=34, size=13, color="#64748B"),
                            username_field,
                            email_field,
                            password_field,
                            ft.Text(f"{session_count} chats", width=84, size=13, color="#64748B"),
                            ft.ElevatedButton(
                                "Save",
                                on_click=save_user,
                                height=40,
                                bgcolor="#087879",
                                color="white",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        wrap=True,
                    ),
                )

            return ft.Container(
                expand=True,
                bgcolor="#FFFFFF" if not is_dark else "#111827",
                border=ft.Border.all(1, "#E5E7EB" if not is_dark else "#1F2937"),
                border_radius=10,
                padding=20,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Users", size=22, weight=ft.FontWeight.BOLD, color=content_text),
                                        ft.Text("Admin can edit account details. User chats stay separated by username.", size=12, color="#64748B"),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.Container(
                                    content=ft.Text("Admin", color="#087879", size=12, weight=ft.FontWeight.BOLD),
                                    bgcolor="#D9F6F8",
                                    border_radius=14,
                                    padding=ft.padding.Padding(left=10, top=6, right=10, bottom=6),
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Text(admin_message, color=status_color, size=12) if admin_message else ft.Container(height=0),
                        ft.Container(
                            content=ft.Column([build_user_row(user) for user in all_users], spacing=10, scroll=ft.ScrollMode.AUTO),
                            expand=True,
                        ),
                    ],
                    spacing=14,
                    expand=True,
                ),
            )

        dashboard_stats = build_creative_dashboard_stats(user_data)
        dashboard_view = create_dashboard_view(page, dashboard_stats)
        dashboard_view.visible = current_view == "dashboard" and current_user is not None

        is_dark = page.theme_mode == ft.ThemeMode.DARK
        content_bg = "#060816" if is_dark else "#F7FAFA"
        content_text = "#F8FAFC" if is_dark else "#0F172A"
        sidebar_bg = "#087879"
        sidebar_active = "#24969A"
        sidebar_hover = "#0D8588"
        sidebar_width = 236 if sidebar_open else 72

        def nav_item(label, icon_name, action, active=False):
            item_bg = sidebar_active if active and sidebar_open else sidebar_bg
            if sidebar_open:
                return ft.Container(
                    height=38,
                    border_radius=6,
                    bgcolor=item_bg,
                    padding=ft.padding.Padding(left=14, top=0, right=12, bottom=0),
                    ink=True,
                    on_click=action,
                    content=ft.Row(
                        [
                            ft.Icon(icon_name, color="white", size=16),
                            ft.Text(label, color="white", size=13, weight=ft.FontWeight.W_500),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            return ft.Container(
                height=42,
                border_radius=8,
                bgcolor=sidebar_active if active else sidebar_bg,
                alignment=ft.Alignment(0, 0),
                ink=True,
                on_click=action,
                content=ft.Icon(icon_name, color="white", size=18),
            )

        sidebar_controls = []
        sidebar_controls.append(
            ft.Row(
                [
                    ft.IconButton(
                        ft.Icons.MENU_OPEN_ROUNDED if sidebar_open else ft.Icons.MENU_ROUNDED,
                        on_click=toggle_sidebar,
                        icon_color="white",
                        icon_size=20,
                        tooltip="Close sidebar" if sidebar_open else "Open sidebar",
                    ),
                    ft.IconButton(
                        ft.Icons.BRIGHTNESS_4_ROUNDED if is_dark else ft.Icons.BRIGHTNESS_7_ROUNDED,
                        on_click=toggle_theme,
                        icon_color="white",
                        icon_size=18,
                        tooltip="Light mode" if is_dark else "Night mode",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN if sidebar_open else ft.MainAxisAlignment.CENTER,
            )
        )

        if sidebar_open:
            sidebar_controls.append(ft.Container(height=8))
            sidebar_controls.append(ft.Text("Creator Studio", color="white", size=20, weight=ft.FontWeight.BOLD))
            sidebar_controls.append(ft.Text("AI POWERED", color="#9FD6D8", size=9, weight=ft.FontWeight.W_500))
            sidebar_controls.append(ft.Container(height=26))

        if sidebar_open:
            sidebar_controls.append(
                ft.Container(
                    height=42,
                    border_radius=10,
                    bgcolor=sidebar_active if current_view == "chat" else sidebar_bg,
                    padding=ft.padding.Padding(left=14, top=0, right=12, bottom=0),
                    ink=True,
                    on_click=new_chat,
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.EDIT_ROUNDED, color="white", size=18),
                            ft.Text("New chat", color="white", size=14, weight=ft.FontWeight.W_500),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )
        else:
            sidebar_controls.append(
                ft.Container(
                    height=42,
                    border_radius=8,
                    bgcolor=sidebar_active if current_view == "chat" else sidebar_bg,
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=new_chat,
                    content=ft.Icon(ft.Icons.EDIT_ROUNDED, color="white", size=18),
                )
            )

        sidebar_controls.append(nav_item("Dashboard", ft.Icons.DASHBOARD_ROUNDED, lambda e: (set_view("dashboard"), render()), current_view == "dashboard"))
        if current_user == "Admin":
            sidebar_controls.append(nav_item("Users", ft.Icons.GROUP_ROUNDED, lambda e: (set_view("admin"), render()), current_view == "admin"))
        sidebar_controls.append(nav_item("Song", ft.Icons.MUSIC_NOTE_ROUNDED, open_song_dialog, False))
        sidebar_controls.append(nav_item("Story", ft.Icons.MENU_BOOK_ROUNDED, open_story_dialog, False))

        if sidebar_open:
            sidebar_controls.append(ft.Container(height=18))
            sidebar_controls.append(ft.Text("Recent Sessions", color="#BDE4E5", size=11, weight=ft.FontWeight.BOLD))
            if sessions:
                for session in sessions[-6:]:
                    sidebar_controls.append(
                        ft.Container(
                            height=34,
                            border_radius=6,
                            bgcolor=sidebar_hover if session["title"] == active_session else sidebar_bg,
                            padding=ft.padding.Padding(left=12, top=0, right=8, bottom=0),
                            ink=True,
                            on_click=lambda e, s=session["title"]: load_session(e, s),
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED, color="white", size=14),
                                    ft.Text(session["title"], color="white", size=12, max_lines=1, expand=True),
                                ],
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        )
                    )
            else:
                sidebar_controls.append(ft.Text("No sessions yet", color="#9FD6D8", size=12))

        if sidebar_open:
            sidebar_bottom = ft.Column(
                [
                    ft.Divider(color="#1B8E91", height=18),
                    ft.Row(
                        [
                            ft.Container(
                                width=40,
                                height=40,
                                border_radius=20,
                                bgcolor="#064E4F",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(ft.Icons.PERSON_ROUNDED, color="#F7D5A5", size=22),
                            ),
                            ft.Column(
                                [
                                    ft.Text(user_info.get("username", current_user), color="white", size=15, weight=ft.FontWeight.BOLD, max_lines=1),
                                    ft.Text("Pro Member", color="#BDE4E5", size=12),
                                ],
                                spacing=1,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=8),
                    nav_item("Logout", ft.Icons.LOGOUT_ROUNDED, logout, False),
                ],
                spacing=8,
            )
        else:
            sidebar_bottom = ft.Column(
                [
                    ft.IconButton(ft.Icons.PERSON_ROUNDED, icon_color="white", tooltip=current_user),
                    ft.IconButton(ft.Icons.LOGOUT_ROUNDED, on_click=logout, icon_color="white", tooltip="Logout"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            )

        sidebar = ft.Container(
            width=sidebar_width,
            bgcolor=sidebar_bg,
            padding=ft.padding.Padding(left=14, top=18, right=14, bottom=16),
            content=ft.Column(
                [
                    ft.Column(sidebar_controls, spacing=8, expand=True, scroll=ft.ScrollMode.AUTO),
                    sidebar_bottom,
                ],
                spacing=10,
                expand=True,
            ),
        )

        pending_creator = user_data.get("pending_creator")
        input_controls = [user_input]
        if pending_creator in ("song", "story"):
            creator_icon = ft.Icons.MUSIC_NOTE_ROUNDED if pending_creator == "song" else ft.Icons.MENU_BOOK_ROUNDED
            creator_tooltip = "Open Song Creator" if pending_creator == "song" else "Open Story Creator"
            input_controls.append(
                ft.Container(
                    width=48,
                    height=48,
                    border_radius=14,
                    bgcolor="#D9F6F8",
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    tooltip=creator_tooltip,
                    on_click=reopen_pending_creator,
                    content=ft.Icon(creator_icon, color="#087879", size=22),
                )
            )
        input_controls.append(
            ft.Container(
                width=48,
                height=48,
                border_radius=14,
                bgcolor="#087879",
                alignment=ft.Alignment(0, 0),
                ink=True,
                on_click=send_message,
                content=ft.Icon(ft.Icons.ARROW_UPWARD_ROUNDED, color="white", size=22),
            )
        )

        chat_title = "New chat"
        chat_panel = ft.Column(
            [
                ft.Container(
                    padding=ft.padding.Padding(left=18, top=14, right=18, bottom=14),
                    border=ft.Border(bottom=ft.BorderSide(1, "#E5E7EB" if not is_dark else "#1F2937")),
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(chat_title, size=18, weight=ft.FontWeight.BOLD, color=content_text, max_lines=1),
                                    ft.Text("Poet AI is ready for songs, poems, and stories", size=12, color="#6B7280" if not is_dark else "#A7B0BF"),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.Text("AI", color="#087879", size=12, weight=ft.FontWeight.BOLD),
                                bgcolor="#D9F6F8",
                                border_radius=14,
                                padding=ft.padding.Padding(left=10, top=6, right=10, bottom=6),
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    content=chat_history,
                    expand=True,
                    padding=ft.padding.Padding(left=18, top=18, right=18, bottom=4),
                ),
                ft.Container(
                    padding=ft.padding.Padding(left=18, top=12, right=18, bottom=16),
                    border=ft.Border(top=ft.BorderSide(1, "#E5E7EB" if not is_dark else "#1F2937")),
                    content=ft.Row(
                        input_controls,
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                ),
            ],
            spacing=0,
            expand=True,
        )

        if current_view == "dashboard":
            main_content = dashboard_view
        elif current_view == "admin" and current_user == "Admin":
            main_content = build_admin_users_view()
        else:
            main_content = ft.Container(
                expand=True,
                border_radius=10,
                bgcolor="#FFFFFF" if not is_dark else "#111827",
                border=ft.Border.all(1, "#E5E7EB" if not is_dark else "#1F2937"),
                content=chat_panel,
            )

        content_area = ft.Container(
            expand=True,
            bgcolor=content_bg,
            padding=20,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Poet AI", size=26, weight=ft.FontWeight.BOLD, color=content_text),
                                    ft.Text("Creative chat workspace", size=12, color="#6B7280" if not is_dark else "#A7B0BF"),
                                ],
                                spacing=2,
                            ),
                            ft.IconButton(ft.Icons.LOGOUT_ROUNDED, on_click=logout, icon_color=content_text),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=12),
                    main_content,
                ],
                expand=True,
                spacing=0,
            ),
        )
        return ft.Row([sidebar, content_area], expand=True)

    def set_view(view_name):
        nonlocal current_view
        current_view = view_name

    def render():
        page.controls.clear()
        if current_view == "home":
            page.add(build_home_view())
        elif current_view == "login":
            page.add(build_auth_view("login"))
        elif current_view == "signup":
            page.add(build_auth_view("signup"))
        elif current_view in ("dashboard", "chat", "admin"):
            if current_user is None:
                set_view("home")
                page.add(build_home_view())
            elif current_view == "admin" and current_user != "Admin":
                set_view("dashboard")
                page.add(build_dashboard_view())
            else:
                page.add(build_dashboard_view())
        page.update()

    render()


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))

    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER,
        host=host,
        port=port,
    )