# ./src/app.py
# src/app.py
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps
import os
from src.core.logging import logger, TRACE
from dotenv import load_dotenv

from src.components.chat_list import ChatList
from src.components.utility_bar import UtilityBar
from src.components.chat.widget import ChatInterface
from src.components.settings.window import SettingsWindow
from src.utils import get_theme_colors, theme_names, get_default_button_color

# Load environment variables from .env if present
load_dotenv()

class MailSocialApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mail Social")
        self.geometry("1024x768")

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Get the current theme colors and set default font size
        self.accent_color = get_default_button_color(ctk.get_appearance_mode().lower())  # Store the current accent color
        self.update_colors()
        self.font_size = tk.IntVar(value=12)  # Default font size

        # Left sidebar frame with chat list and utility bar
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.colors["primary"], width=300)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_propagate(False)

        self.chat_list = ChatList(self.sidebar_frame, self.colors, self.font_size)
        self.chat_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        self.utility_bar = UtilityBar(self.sidebar_frame, self.colors, self.open_settings)
        self.utility_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        # Right main frame with chat interface
        self.main_frame = ChatInterface(self, self.colors)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(1, 0), pady=0)

    def send_message(self):
        message = self.main_frame.message_frame.get_message()
        if message:
            self.main_frame.display_message(f"You: {message}")
            self.main_frame.message_frame.clear_message()
            logger.info(f"Message sent: {message}")

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.grab_set()

    def update_colors(self):
        current_theme = ctk.get_appearance_mode().lower()
        self.colors = get_theme_colors(current_theme)
        self.colors["button"] = self.accent_color
        logger.trace(f"Updated colors to: {self.colors}")
        self.apply_colors()

    def apply_colors(self):
        # Apply colors to all components
        if hasattr(self, 'chat_list'):
            self.chat_list.update_colors(self.colors)
        if hasattr(self, 'main_frame'):
            self.main_frame.update_colors(self.colors)
        if hasattr(self, 'utility_bar'):
            self.utility_bar.update_colors(self.colors)
        if hasattr(self, 'sidebar_frame'):
            self.sidebar_frame.configure(fg_color=self.colors["primary"])

    def update_font_size(self, new_size):
        self.font_size.set(new_size)
        self.chat_list.update_font_size(new_size)
        logger.info(f"Updated font size to: {new_size}")

    def update_accent_color(self, color):
        self.accent_color = color
        self.update_colors()
        logger.info(f"Updated accent color to: {color}")

if __name__ == "__main__":
    app = MailSocialApp()
    app.mainloop()
