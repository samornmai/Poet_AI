# Responsive Design Guide - Poet AI Studio

## Overview
Your Poet AI Studio app now has full responsive design support for web and mobile devices. This guide explains how the system works and how to apply it to other screens.

---

## Responsive Breakpoints

The app uses three main breakpoints to adapt layouts:

| Device Type | Width | Class | Use Case |
|-------------|-------|-------|----------|
| **Mobile** | < 600px | `is_mobile` | Phones, small devices |
| **Tablet** | 600-900px | `is_tablet` | Tablets, medium devices |
| **Desktop** | ≥ 900px | `is_desktop` | Large screens |

---

## Key Files

### 1. **responsive.py** (NEW)
Central configuration for responsive design. Contains:
- `ResponsiveConfig` class - provides responsive values based on screen width
- Breakpoint constants
- Responsive properties: padding, font sizes, button dimensions, spacing, card widths

### 2. **main.py** (UPDATED)
- Imports responsive utilities
- Detects window resize events
- Auto-hides sidebar on mobile (< 600px)
- Updates layout when screen size changes

### 3. **sidebar.py** (UPDATED)
- Now takes optional `page_width` parameter
- Responsive width based on screen size
- Adapts to mobile by becoming invisible

### 4. **home.py** (UPDATED)
- Uses `ResponsiveConfig` for adaptive sizing
- Responsive typography (sizes change per breakpoint)
- Buttons wrap on mobile
- Cards stack on mobile, 3-per-row on desktop

### 5. **Screen/dashboard.py** (UPDATED)
- Responsive card grid (1 column mobile, 2 tablet, 3 desktop)
- Adaptive dialogs (smaller on mobile)
- Responsive typography and spacing

---

## How to Use Responsive Design

### Quick Start: Import and Use Config

```python
from responsive import ResponsiveConfig

def my_screen(nav_callback):
    config = ResponsiveConfig(1200)  # Default width
    
    # Use config properties:
    padding = config.main_padding           # Adaptive padding
    font_size = config.heading_size         # Adaptive font (24-40px)
    button_height = config.button_height    # Adaptive button height
    button_width = config.button_width      # Adaptive button width
    card_width = config.card_width          # Adaptive card width
    spacing = config.spacing_medium         # Adaptive spacing
    
    # Check device type
    if config.is_mobile:
        # Mobile-specific code
    elif config.is_tablet:
        # Tablet-specific code
    else:
        # Desktop-specific code
```

### Available ResponsiveConfig Properties

```python
config.is_mobile              # Boolean: True if < 600px
config.is_tablet              # Boolean: True if 600-900px
config.is_desktop             # Boolean: True if >= 900px

config.main_padding           # Container padding (left/right/top/bottom)
config.card_padding           # Card padding
config.heading_size           # Main heading font size (24-40px)
config.subheading_size        # Subheading font size (14-18px)
config.body_text_size         # Body text size (12-14px)
config.button_height          # Button height (40-50px)
config.button_width           # Button width (None on mobile = full width)
config.cards_per_row          # Cards per row in grid (1-3)
config.card_width             # Card width (None on mobile = full width)
config.sidebar_width          # Sidebar width (0 on mobile, 240-260px on desktop)
config.spacing_small          # Small spacing (8-12px)
config.spacing_medium         # Medium spacing (12-16px)
config.spacing_large          # Large spacing (16-24px)
```

---

## Implementation Examples

### Example 1: Responsive Text Sizes

```python
from responsive import ResponsiveConfig
import flet as ft

config = ResponsiveConfig(page.width)

title = ft.Text(
    "My Title",
    size=config.heading_size,  # 24px mobile, 40px desktop
    weight=ft.FontWeight.BOLD
)

body = ft.Text(
    "Body text",
    size=config.body_text_size  # 12px mobile, 14px desktop
)
```

### Example 2: Responsive Button Layout

```python
buttons_row = ft.Row([
    ft.ElevatedButton(
        "Save",
        width=config.button_width,       # None on mobile (full width)
        height=config.button_height,     # 40px mobile, 50px desktop
    ),
    ft.ElevatedButton("Cancel", width=config.button_width, height=config.button_height),
],
wrap=True,  # Important! Wraps on mobile
spacing=config.spacing_medium
)
```

### Example 3: Responsive Card Grid

```python
cards = ft.Row([
    create_card(...),  # width=config.card_width adapts automatically
    create_card(...),
    create_card(...),
],
wrap=True,  # Cards wrap to new row on mobile/tablet
spacing=config.spacing_large
)
```

### Example 4: Conditional Mobile Layout

```python
if config.is_mobile:
    # Show stacked layout on mobile
    layout = ft.Column([...])
else:
    # Show side-by-side layout on desktop
    layout = ft.Row([...])
```

### Example 5: Responsive Containers

```python
container = ft.Container(
    content=ft.Column([...]),
    padding=config.main_padding,  # Adapts to screen size
    width=config.card_width,      # Adapts or None (full width)
    border_radius=12,
)
```

---

## Mobile Design Best Practices

### DO ✅

- Use `wrap=True` on Rows to allow wrapping on mobile
- Use `None` for width on mobile to allow full-width elements
- Use responsive font sizes from config
- Use `ft.Column` for mobile stacked layouts
- Test on multiple screen sizes
- Use proper spacing from config properties

### DON'T ❌

- Hard-code pixel values (use config properties instead)
- Use fixed widths for buttons/cards on mobile
- Use small font sizes (< 12px) that are hard to read
- Create horizontal scrolling layouts
- Use Rows with many items without `wrap=True`

---

## Sidebar Behavior

The sidebar is automatically hidden on mobile devices:

- **Mobile (< 600px)**: Sidebar hidden, content full-width
- **Tablet (600-900px)**: Sidebar visible (240px)
- **Desktop (≥ 900px)**: Sidebar visible (260px)

To manually hide/show sidebar in custom screens:

```python
sidebar.visible = not config.is_mobile
```

---

## Testing Responsive Design

### In Browser
1. Open your Flet web app at `http://localhost:8000`
2. Press `F12` to open Developer Tools
3. Click Device Toolbar (Ctrl+Shift+M) to toggle mobile view
4. Try different screen widths to see responsive behavior

### Screen Sizes to Test
- **Mobile**: 375x667 (iPhone), 414x896 (Android)
- **Tablet**: 768x1024 (iPad), 800x1280 (Android Tablet)
- **Desktop**: 1920x1080, 1366x768

---

## Performance Tips

- The `ResponsiveConfig` object is lightweight and created once per view
- Responsive values are computed once on screen load
- Resize events trigger minimal updates (only visibility changes for sidebar)
- No performance impact from using responsive design

---

## Future Enhancements

To further improve responsiveness:

1. **Add hamburger menu** for mobile navigation
2. **Bottom navigation bar** for mobile (tab bar style)
3. **Landscape mode support** for mobile devices
4. **Portrait/landscape orientation detection**
5. **Touch-friendly tap targets** (larger buttons on mobile)

---

## Troubleshooting

### Issue: Content not wrapping on mobile
**Solution**: Add `wrap=True` to Row/Column containing items

### Issue: Text too small on mobile
**Solution**: Use `config.body_text_size` instead of hard-coded values

### Issue: Sidebar not hiding on mobile
**Solution**: Ensure `sidebar_layout.visible = not config.is_mobile` in switch_workspace_view()

### Issue: Buttons overlapping on mobile
**Solution**: Use `width=None` for full-width buttons or `wrap=True` on container

---

## Questions?

For more info about Flet's responsive features, visit:
- https://flet.dev/docs/controls/responsive
- https://flet.dev/docs/guides/responsive-design

