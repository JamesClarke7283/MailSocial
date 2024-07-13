# ./src/components/settings/appearance.py
# src/components/settings/appearance.py
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

from src.core.logging import logger
from src.utils import (
    get_accents,
    get_default_button_color,
    get_theme_colors,
    theme_names,
)


class AppearanceSettings(ctk.CTkFrame):
    def __init__(self, master, parent, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.parent = parent
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:")
        self.appearance_mode_label.pack(pady=10)

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(
            self, values=theme_names, command=self.change_appearance_mode
        )
        self.appearance_mode_optionmenu.set(ctk.get_appearance_mode())
        self.appearance_mode_optionmenu.pack(pady=10)

        self.font_size_label = ctk.CTkLabel(self, text="Font Size:")
        self.font_size_label.pack(pady=10)

        self.font_size_slider = ctk.CTkSlider(
            self, from_=8, to=20, number_of_steps=12, command=self.change_font_size
        )
        self.font_size_slider.set(self.parent.parent.font_size.get())
        self.font_size_slider.pack(pady=10)

        self.font_size_value_label = ctk.CTkLabel(
            self, text=f"Font Size: {self.parent.parent.font_size.get()}"
        )
        self.font_size_value_label.pack(pady=5)

        self.accent_color_label = ctk.CTkLabel(self, text="Accent Color:")
        self.accent_color_label.pack(pady=10)

        self.accent_palette = ctk.CTkFrame(self)
        self.accent_palette.pack(pady=10)

        self.selected_accent = None
        self.accent_buttons = []
        self.load_accents()

    def load_accents(self):
        accents = get_accents()
        current_theme = ctk.get_appearance_mode().lower()
        default_button_color = get_default_button_color(current_theme)

        # Add a button for default accent color
        default_button = ctk.CTkButton(
            self.accent_palette,
            text="Default",
            fg_color=default_button_color,
            width=40,
            height=40,
            corner_radius=20,
            command=lambda: self.change_accent_color(
                default_button_color, default_button
            ),
        )
        default_button.pack(side="left", padx=5, pady=5)
        self.accent_buttons.append(default_button)
        self.set_accent_button_border(default_button, selected=True)

        for accent_name, color in accents.items():
            button = ctk.CTkButton(
                self.accent_palette,
                text="",
                fg_color=color,
                width=40,
                height=40,
                corner_radius=20,
            )
            button.configure(
                command=lambda btn=button, clr=color: self.change_accent_color(clr, btn)
            )
            button.pack(side="left", padx=5, pady=5)
            self.accent_buttons.append(button)

    def set_accent_button_border(self, button, selected):
        if selected:
            mode = ctk.get_appearance_mode().lower()
            ring_color = "#ffffff" if mode == "dark" else "#666666"
            button.configure(border_color=ring_color, border_width=2)
        else:
            # Use cget to get the current fg_color
            button.configure(border_color=button.cget("fg_color"), border_width=0)

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode.lower())
        self.parent.update_colors()
        logger.info(f"Changed appearance mode to: {mode}")

    def change_font_size(self, value):
        new_size = int(value)
        self.font_size_value_label.configure(text=f"Font Size: {new_size}")
        self.parent.update_font_size(new_size)
        logger.info(f"Changed font size to: {new_size}")

    def change_accent_color(self, color, button):
        if self.selected_accent:
            self.set_accent_button_border(self.selected_accent, selected=False)
        self.selected_accent = button
        if self.selected_accent:
            self.set_accent_button_border(self.selected_accent, selected=True)

        self.parent.parent.update_accent_color(color)
        logger.info(f"Changed accent color to: {color}")

    def update_colors(self):
        current_theme = ctk.get_appearance_mode().lower()
        colors = get_theme_colors(current_theme)
        self.appearance_mode_label.configure(text_color=colors["text"])
        self.font_size_label.configure(text_color=colors["text"])
        self.font_size_value_label.configure(text_color=colors["text"])
        self.accent_color_label.configure(text_color=colors["text"])
        for button in self.accent_buttons:
            button.configure(fg_color=button.cget("fg_color"))
