import os
import tkinter as tk

import customtkinter as ctk
from dotenv import load_dotenv
from PIL import Image, ImageOps

from src.components.chat.widget import ChatInterface
from src.components.chat_list import ChatList
from src.components.compose.window import ComposeWindow
from src.components.settings.window import SettingsWindow
from src.components.utility_bar import UtilityBar
from src.core.logging import TRACE, logger
from src.utils import get_default_button_color, get_theme_colors, theme_names

# Load environment variables from .env if present
load_dotenv()


class MailSocialApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Mail Social")
        self.geometry("1024x768")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.accent_color = get_default_button_color(ctk.get_appearance_mode().lower())
        self.update_colors()
        self.font_size = tk.IntVar(value=12)

        self.sidebar_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=self.colors["primary"], width=300
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_propagate(False)

        self.chat_list = ChatList(self.sidebar_frame, self.colors, self.font_size, self)
        self.chat_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        self.utility_bar = UtilityBar(
            self.sidebar_frame, self.colors, self.open_settings
        )
        self.utility_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.main_frame = ChatInterface(self, self.colors)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(1, 0), pady=0)

    def send_message(self) -> None:
        message = self.main_frame.message_frame.get_message()
        if message:
            self.main_frame.display_message(message, "You", True)
            self.main_frame.message_frame.clear_message()
            logger.info(f"Message sent: {message}")

    def open_settings(self) -> None:
        settings_window = SettingsWindow(self)
        settings_window.grab_set()

    def update_colors(self) -> None:
        current_theme = ctk.get_appearance_mode().lower()
        self.colors = get_theme_colors(current_theme)
        self.colors["button"] = self.accent_color
        logger.trace(f"Updated colors to: {self.colors}")
        self.apply_colors()

    def apply_colors(self) -> None:
        if hasattr(self, "chat_list"):
            self.chat_list.update_colors(self.colors)
        if hasattr(self, "main_frame"):
            self.main_frame.update_colors(self.colors)
        if hasattr(self, "utility_bar"):
            self.utility_bar.update_colors(self.colors)
        if hasattr(self, "sidebar_frame"):
            self.sidebar_frame.configure(fg_color=self.colors["primary"])

    def update_font_size(self, new_size: int) -> None:
        self.font_size.set(new_size)
        self.chat_list.update_font_size(new_size)
        logger.info(f"Updated font size to: {new_size}")

    def update_accent_color(self, color: str) -> None:
        self.accent_color = color
        self.update_colors()
        logger.info(f"Updated accent color to: {color}")

    def display_chat(self, chat: ChatInterface) -> None:
        self.main_frame.display_chat(chat)

    def open_compose_window(self) -> None:
        compose_window = ComposeWindow(self)
        self.wait_visibility(
            compose_window
        )  # Ensure window is viewable before grabbing
        compose_window.grab_set()


if __name__ == "__main__":
    app = MailSocialApp()
    app.mainloop()
