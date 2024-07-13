import customtkinter as ctk
from typing import Any

from .appearance import AppearanceSettings


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent: Any) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.geometry("400x500")

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.appearance_tab = self.tab_view.add("Appearance")
        self.appearance_settings = AppearanceSettings(self.appearance_tab, parent=self)

        # Set the default tab
        self.tab_view.set("Appearance")

    def update_colors(self) -> None:
        self.appearance_settings.update_colors()

    def update_font_size(self, new_size: int) -> None:
        self.appearance_settings.update_font_size(new_size)

    def update_accent_color(self, color: str) -> None:
        self.parent.update_accent_color(color)