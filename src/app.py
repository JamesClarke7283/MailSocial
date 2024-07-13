# src/app.py
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps
import tomllib
import os
from src.core.logging import logger, TRACE
from dotenv import load_dotenv

from src.components.chat_list import ChatList
from src.components.utility_bar import UtilityBar
from src.components.chat.widget import ChatInterface

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

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Get the current theme colors and set default font size
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
        self.colors = get_theme_colors(ctk.get_appearance_mode().lower())
        logger.trace(f"Updated colors to: {self.colors}")

    def update_font_size(self, new_size):
        self.font_size.set(new_size)
        self.chat_list.update_font_size(new_size)
        logger.info(f"Updated font size to: {new_size}")

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.geometry("400x400")

        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:")
        self.appearance_mode_label.pack(pady=10)

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self, values=theme_names,
                                                            command=self.change_appearance_mode)
        self.appearance_mode_optionmenu.set(ctk.get_appearance_mode())
        self.appearance_mode_optionmenu.pack(pady=10)

        self.font_size_label = ctk.CTkLabel(self, text="Font Size:")
        self.font_size_label.pack(pady=10)

        self.font_size_slider = ctk.CTkSlider(self, from_=8, to=20, number_of_steps=12,
                                              command=self.change_font_size)
        self.font_size_slider.set(self.parent.font_size.get())
        self.font_size_slider.pack(pady=10)

        self.font_size_value_label = ctk.CTkLabel(self, text=f"Font Size: {self.parent.font_size.get()}")
        self.font_size_value_label.pack(pady=5)

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode.lower())
        self.parent.update_colors()
        logger.info(f"Changed appearance mode to: {mode}")

    def change_font_size(self, value):
        new_size = int(value)
        self.font_size_value_label.configure(text=f"Font Size: {new_size}")
        self.parent.update_font_size(new_size)
        logger.info(f"Changed font size to: {new_size}")

if __name__ == "__main__":
    app = MailSocialApp()
    app.mainloop()