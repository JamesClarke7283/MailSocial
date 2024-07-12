# src/app.py
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps
import tomllib
import os
from src.core.logging import logger, TRACE
from dotenv import load_dotenv

from src.components.chat_list import ChatList
from src.components.chat_interface import ChatInterface
from src.components.utility_bar import UtilityBar

# Load environment variables from .env if present
load_dotenv()

# Read themes from the .default_settings.toml file
with open(".default_settings.toml", "rb") as f:
    config = tomllib.load(f)

themes = config["themes"]
theme_names = [theme.capitalize() for theme in themes.keys()]

def get_theme_colors(theme_name):
    return themes[theme_name.lower()]

class MailSocialApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mail Social")
        self.geometry("1024x768")

        # Configure grid layout (2x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Get the current theme colors
        self.update_colors()

        # Left sidebar frame with chat list and utility bar
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.colors["primary"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=0)

        self.chat_list = ChatList(self.sidebar_frame, self.colors)
        self.chat_list.grid(row=0, column=0, sticky="nsew")

        self.utility_bar = UtilityBar(self.sidebar_frame, self.colors, self.open_settings)
        self.utility_bar.grid(row=1, column=0, sticky="sew")

        # Right main frame with chat interface
        self.main_frame = ChatInterface(self, self.colors)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def send_message(self):
        message = self.main_frame.message_entry.get()
        if message:
            self.main_frame.display_message(f"You: {message}")
            self.main_frame.message_entry.delete(0, "end")
            logger.info(f"Message sent: {message}")

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.grab_set()

    def update_colors(self):
        self.colors = get_theme_colors(ctk.get_appearance_mode().lower())
        logger.trace(f"Updated colors to: {self.colors}")

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.geometry("400x300")

        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:")
        self.appearance_mode_label.pack(pady=10)

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self, values=theme_names,
                                                            command=self.change_appearance_mode)
        self.appearance_mode_optionmenu.set(ctk.get_appearance_mode())
        self.appearance_mode_optionmenu.pack(pady=10)

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode.lower())
        self.parent.update_colors()
        logger.info(f"Changed appearance mode to: {mode}")

if __name__ == "__main__":
    app = MailSocialApp()
    app.mainloop()
