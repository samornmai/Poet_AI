"""
Responsive design utilities for Poet AI Studio
Handles breakpoints and responsive configurations for web and mobile
"""
import flet as ft

# Responsive breakpoints
BREAKPOINT_MOBILE = 600      # Mobile devices
BREAKPOINT_TABLET = 900      # Tablets
BREAKPOINT_DESKTOP = 1200    # Desktop

class ResponsiveConfig:
    """Configuration class for responsive values based on page width"""
    
    def __init__(self, page_width):
        self.page_width = page_width
        self.is_mobile = page_width < BREAKPOINT_MOBILE
        self.is_tablet = BREAKPOINT_MOBILE <= page_width < BREAKPOINT_TABLET
        self.is_desktop = page_width >= BREAKPOINT_TABLET
    
    @property
    def main_padding(self):
        """Main content padding"""
        if self.is_mobile:
            return ft.padding.Padding(left=16, top=12, right=16, bottom=12)
        elif self.is_tablet:
            return ft.padding.Padding(left=24, top=20, right=24, bottom=20)
        else:
            return ft.padding.Padding(left=40, top=40, right=40, bottom=40)
    
    @property
    def card_padding(self):
        """Card padding"""
        if self.is_mobile:
            return ft.padding.Padding(left=12, top=12, right=12, bottom=12)
        elif self.is_tablet:
            return ft.padding.Padding(left=16, top=16, right=16, bottom=16)
        else:
            return ft.padding.Padding(left=24, top=24, right=24, bottom=24)
    
    @property
    def heading_size(self):
        """Main heading size"""
        if self.is_mobile:
            return 24
        elif self.is_tablet:
            return 32
        else:
            return 40
    
    @property
    def subheading_size(self):
        """Subheading size"""
        if self.is_mobile:
            return 14
        elif self.is_tablet:
            return 16
        else:
            return 18
    
    @property
    def body_text_size(self):
        """Body text size"""
        if self.is_mobile:
            return 12
        elif self.is_tablet:
            return 13
        else:
            return 14
    
    @property
    def button_height(self):
        """Button height"""
        if self.is_mobile:
            return 40
        elif self.is_tablet:
            return 44
        else:
            return 50
    
    @property
    def button_width(self):
        """Button width"""
        if self.is_mobile:
            return None  # Full width
        elif self.is_tablet:
            return 180
        else:
            return 200
    
    @property
    def cards_per_row(self):
        """Number of cards per row"""
        if self.is_mobile:
            return 1
        elif self.is_tablet:
            return 2
        else:
            return 3
    
    @property
    def card_width(self):
        """Card width"""
        if self.is_mobile:
            return None  # Full width
        elif self.is_tablet:
            return 280
        else:
            return 320
    
    @property
    def sidebar_width(self):
        """Sidebar width"""
        if self.is_mobile:
            return 0  # Hidden on mobile
        elif self.is_tablet:
            return 240
        else:
            return 260
    
    @property
    def spacing_small(self):
        """Small spacing"""
        return 8 if self.is_mobile else 12
    
    @property
    def spacing_medium(self):
        """Medium spacing"""
        return 12 if self.is_mobile else 16
    
    @property
    def spacing_large(self):
        """Large spacing"""
        return 16 if self.is_mobile else 24


def get_responsive_config(page):
    """Helper function to get responsive config"""
    return ResponsiveConfig(page.width)
