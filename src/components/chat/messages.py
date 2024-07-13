import tkinter as tk
from datetime import datetime
import customtkinter as ctk
from typing import List, Dict, Any

class ChatMessages(ctk.CTkFrame):
    def __init__(self, master: Any, colors: Dict[str, str], *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.configure(fg_color=self.colors["secondary"], corner_radius=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.message_frame = ctk.CTkScrollableFrame(
            self, fg_color=self.colors["secondary"]
        )
        self.message_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.message_frame.grid_columnconfigure(0, weight=1)

        self.message_widgets: List[ctk.CTkFrame] = []

    def display_message(self, message: str, sender: str, is_user: bool) -> None:
        bubble_color = self.colors["button"] if is_user else self.colors["primary"]
        anchor = "e" if is_user else "w"
        justify = "right" if is_user else "left"
        text_color = self.colors["button_text"] if is_user else self.colors["text"]

        sender_name = sender if sender != "You" else ""
        sender_color = "#007AFF" if is_user else "#34C759"

        message_frame = ctk.CTkFrame(
            self.message_frame, fg_color=bubble_color, corner_radius=10
        )
        message_frame.grid_columnconfigure(0, weight=1)
        message_frame.grid(
            row=len(self.message_widgets), column=0, sticky="ew", padx=10, pady=5
        )

        if sender_name:
            sender_label = ctk.CTkLabel(
                message_frame,
                text=sender_name,
                anchor=anchor,
                justify=justify,
                text_color=sender_color,
                fg_color=bubble_color,
                corner_radius=10,
                font=("Arial", 12, "bold"),
            )
            sender_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 0))

        message_label = ctk.CTkLabel(
            message_frame,
            text=message,
            anchor=anchor,
            justify=justify,
            text_color=text_color,
            fg_color=bubble_color,
            corner_radius=10,
            padx=10,
            pady=5,
        )
        message_label.grid(
            row=1 if sender_name else 0, column=0, sticky="ew", padx=10, pady=(0, 5)
        )

        timestamp_label = ctk.CTkLabel(
            message_frame,
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            anchor=anchor,
            justify=justify,
            text_color=text_color,
            fg_color=bubble_color,
            corner_radius=10,
            padx=10,
            pady=5,
            font=("Arial", 10),
        )
        timestamp_label.grid(
            row=2 if sender_name else 1, column=0, sticky="ew", padx=10, pady=(0, 5)
        )

        self.message_widgets.append(message_frame)

    def clear_messages(self) -> None:
        for widget in self.message_widgets:
            widget.destroy()
        self.message_widgets = []

    def update_colors(self, colors: Dict[str, str]) -> None:
        self.colors = colors
        self.configure(fg_color=self.colors["secondary"])
        for widget in self.message_widgets:
            widget.configure(
                fg_color=self.colors["secondary"], text_color=self.colors["text"]
            )