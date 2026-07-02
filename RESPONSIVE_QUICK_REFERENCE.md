# Responsive Design Quick Reference

## One-Minute Setup

```python
from responsive import ResponsiveConfig
import flet as ft

def my_screen(nav_callback):
    config = ResponsiveConfig(1200)
    
    # Your responsive UI
    return ft.Container(
        content=ft.Column([
            ft.Text("Title", size=config.heading_size),
            ft.ElevatedButton(
                "Click me",
                width=config.button_width,
                height=config.button_height,
            )
        ]),
        padding=config.main_padding,
    )
```

---

## Breakpoints at a Glance

```
Mobile         Tablet         Desktop
(< 600px)      (600-900px)    (≥ 900px)
─────────      ──────────     ─────────
┌─────────┐   ┌──────────┐   ┌─────────────┐
│ Content │   │ Sidebar  │   │  Sidebar    │
│  Full   │   │ Sidebar  │   │ Content     │
│  Width  │   │ Content  │   │             │
└─────────┘   └──────────┘   └─────────────┘
Card: 1 col   Card: 2 cols   Card: 3 cols
Size: 24px    Size: 32px     Size: 40px
Hide sidebar  Show 240px     Show 260px
```

---

## Most Used Properties

| Use Case | Property | Mobile | Tablet | Desktop |
|----------|----------|--------|--------|---------|
| Title size | `heading_size` | 24px | 32px | 40px |
| Body size | `body_text_size` | 12px | 13px | 14px |
| Button size | `button_height` | 40px | 44px | 50px |
| Button width | `button_width` | None | 180px | 200px |
| Container width | `card_width` | None | 280px | 320px |
| Padding | `main_padding` | 16px | 24px | 40px |
| Spacing | `spacing_large` | 16px | 24px | 24px |

---

## Common Patterns

### Pattern 1: Responsive Text
```python
title = ft.Text("My Title", size=config.heading_size)
```

### Pattern 2: Responsive Buttons
```python
button = ft.ElevatedButton(
    "Save",
    width=config.button_width,    # None on mobile = full width
    height=config.button_height,
)
```

### Pattern 3: Responsive Cards
```python
ft.Row([
    card1, card2, card3
], wrap=True, spacing=config.spacing_large)
```

### Pattern 4: Responsive Container
```python
ft.Container(
    content=content,
    padding=config.main_padding,
    width=config.card_width,
)
```

### Pattern 5: Mobile Check
```python
if config.is_mobile:
    layout = mobile_layout
else:
    layout = desktop_layout
```

---

## Device Classes

```python
config.is_mobile      # < 600px
config.is_tablet      # 600-900px
config.is_desktop     # >= 900px
```

---

## Important: Wrapping

Always use `wrap=True` on Row elements for mobile responsiveness:

```python
# ✅ CORRECT
ft.Row([items], wrap=True, spacing=config.spacing_large)

# ❌ WRONG
ft.Row([items], spacing=20)  # Won't wrap, causes overflow
```

---

## Font Sizes Hierarchy

```
heading_size      → Page titles (24-40px)
subheading_size   → Section titles (14-18px)
body_text_size    → Body text (12-14px)
```

---

## Spacing Levels

```
spacing_small     → Between related items (8-12px)
spacing_medium    → Between sections (12-16px)
spacing_large     → Between major sections (16-24px)
```

---

## Sidebar Behavior

```
Mobile:  Hidden (width = 0px)
Tablet:  Visible (width = 240px)
Desktop: Visible (width = 260px)
```

Auto-managed in `main.py` - no extra code needed!

---

## Checklist for New Screens

- [ ] Import `ResponsiveConfig`
- [ ] Create `config = ResponsiveConfig(1200)`
- [ ] Replace all hard-coded sizes with config properties
- [ ] Add `wrap=True` to Row elements
- [ ] Use `width=None` on mobile for full-width elements
- [ ] Use `padding=config.main_padding`
- [ ] Test on mobile (375px), tablet (768px), desktop (1200px)

---

## Testing Commands

Mobile test:
```
Browser DevTools → Toggle Device Toolbar (Ctrl+Shift+M) → iPhone 12
```

Resize test:
```
Drag browser window edge to change width
Layout should adapt automatically
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Text too small | Use `config.body_text_size` not hard-coded |
| Buttons overlap | Add `wrap=True` to Row, use `width=None` on mobile |
| Sidebar not hiding | Check `sidebar.visible = not config.is_mobile` |
| Content doesn't wrap | Use `wrap=True` on Row element |
| Too much padding | Use `main_padding` instead of hard-coded values |

---

## Size Summary Table

```
MOBILE (< 600px)      TABLET (600-900px)    DESKTOP (≥ 900px)
────────────────      ──────────────────    ─────────────────
H1: 24px              H1: 32px              H1: 40px
Body: 12px            Body: 13px            Body: 14px
Btn: 40px tall        Btn: 44px tall        Btn: 50px tall
Btn: Full width       Btn: 180px            Btn: 200px
Card: Full width      Card: 280px           Card: 320px
Card grid: 1 col      Card grid: 2 cols     Card grid: 3 cols
Padding: 16px         Padding: 24px         Padding: 40px
No sidebar            240px sidebar         260px sidebar
```

---

## Real Example: Song Generator

```python
from responsive import ResponsiveConfig
import flet as ft

def build_song_generate_view(nav_callback):
    config = ResponsiveConfig(1200)
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Song Generator", size=config.heading_size),
            ft.Text(
                "Create beautiful lyrics",
                size=config.body_text_size,
                color="#666"
            ),
            ft.TextField(
                label="Lyrics idea",
                min_lines=3,
                max_lines=6 if not config.is_mobile else 4,
            ),
            ft.Row([
                ft.ElevatedButton(
                    "Generate",
                    width=config.button_width,
                    height=config.button_height,
                ),
                ft.OutlinedButton(
                    "Cancel",
                    width=config.button_width,
                    height=config.button_height,
                ),
            ], wrap=True, spacing=config.spacing_medium),
        ], spacing=config.spacing_large),
        padding=config.main_padding,
    )
```

---

## Files to Know

| File | Purpose |
|------|---------|
| `responsive.py` | Core responsive system |
| `main.py` | App setup with responsive integration |
| `sidebar.py` | Responsive sidebar |
| `home.py` | Responsive home page (example) |
| `Screen/dashboard.py` | Responsive dashboard (example) |

---

## Next: Apply to All Screens

Copy the responsive pattern to:
1. `Screen/song_generator.py`
2. `Screen/story_generator.py`
3. `AIScreen/ai_song_generator.py`
4. `AIScreen/ai_story_generator.py`
5. `Assistant.py`
6. `auth.py`

Each should follow the same pattern: import → create config → use properties.

---

**Happy responsive coding! 🚀**

