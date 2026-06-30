import flet as ft
from database import register_user, login_user
from session_store import SESSION

# ================= THEME =================
PRIMARY = "#0D6E6E"
BG = "#F4F6FA"


# ================= LOGIN =================
def build_login_view(nav_callback):

    email = ft.TextField(
        label="Email address",
        prefix_icon=ft.Icons.EMAIL,
        width=340,
    )

    password = ft.TextField(
        label="Password",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=340,
    )

    # ---------------- LOGIN ACTION ----------------
    def login(e):
        user = login_user(email.value, password.value)

        if user:
            # ✅ WORKING FIX FOR OLD FLET
            SESSION["user_id"] = user["id"]
            SESSION["username"] = user["username"]
            SESSION["auth_token"] = user["auth_token"]

            e.page.snack_bar = ft.SnackBar(
                ft.Text(f"Welcome {user['username']} 🎉"),
                bgcolor="#16A34A",
            )
            e.page.snack_bar.open = True

            nav_callback("Dashboard")

        else:
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Invalid email or password"),
                bgcolor="red",
            )
            e.page.snack_bar.open = True

        e.page.update()

    # ---------------- UI CARD ----------------
    card = ft.Container(
        width=420,
        padding=30,
        border_radius=18,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=20, color="#00000020"),
        content=ft.Column(
            [
                ft.Icon(ft.Icons.AUTO_STORIES, size=50, color=PRIMARY),

                ft.Text("Welcome Back", size=26, weight="bold"),
                ft.Text("Login to continue your AI journey", color="#6B7280"),

                ft.Divider(height=20),

                email,
                password,

                ft.Container(height=10),

                ft.ElevatedButton(
                    "Login",
                    width=340,
                    height=45,
                    bgcolor=PRIMARY,
                    color="white",
                    on_click=login,
                ),

                ft.TextButton(
                    "Create new account",
                    on_click=lambda _: nav_callback("Signup"),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    # ---------------- CENTER FIX ----------------
    return ft.Container(
        expand=True,
        bgcolor=BG,
        content=ft.Row(
            controls=[card],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


# ================= SIGNUP =================
def build_signup_view(nav_callback):

    username = ft.TextField(label="Username", width=340)
    email = ft.TextField(label="Email", width=340)
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=340,
    )

    # ---------------- SIGNUP ACTION ----------------
    def signup(e):

        if not username.value or not email.value or not password.value:
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Please fill all fields"),
                bgcolor="orange",
            )
            e.page.snack_bar.open = True
            e.page.update()
            return

        success = register_user(username.value, email.value, password.value)

        if success:
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Account created successfully 🎉"),
                bgcolor="#16A34A",
            )
            nav_callback("Login")
        else:
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Signup failed (email may already exist)"),
                bgcolor="red",
            )

        e.page.snack_bar.open = True
        e.page.update()

    # ---------------- UI CARD ----------------
    card = ft.Container(
        width=420,
        padding=30,
        border_radius=18,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=20, color="#00000020"),
        content=ft.Column(
            [
                ft.Icon(ft.Icons.PERSON_ADD, size=50, color=PRIMARY),

                ft.Text("Create Account", size=26, weight="bold"),
                ft.Text("Join Poet AI and start creating", color="#6B7280"),

                ft.Divider(height=20),

                username,
                email,
                password,

                ft.Container(height=10),

                ft.ElevatedButton(
                    "Sign Up",
                    width=340,
                    height=45,
                    bgcolor=PRIMARY,
                    color="white",
                    on_click=signup,
                ),

                ft.TextButton(
                    "Already have an account?",
                    on_click=lambda _: nav_callback("Login"),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    # ---------------- CENTER FIX ----------------
    return ft.Container(
        expand=True,
        bgcolor=BG,
        content=ft.Row(
            controls=[card],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )