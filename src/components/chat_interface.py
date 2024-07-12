import customtkinter as ctk
import tkinter as tk

class ChatInterface(ctk.CTkFrame):
    def __init__(self, master, colors, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.configure(fg_color=self.colors["primary"], corner_radius=10)

        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Chat display area
        self.chat_display = ctk.CTkFrame(self, corner_radius=10, fg_color=self.colors["secondary"])
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_display.grid_rowconfigure(0, weight=1)
        self.chat_display.grid_columnconfigure(0, weight=1)

        # Message input area
        self.message_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.colors["tertiary"])
        self.message_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.message_frame.grid_columnconfigure(0, weight=1)
        self.message_frame.grid_columnconfigure(1, weight=0)

        self.message_entry = ctk.CTkEntry(self.message_frame, placeholder_text="Write a message...", fg_color=self.colors["primary"], text_color=self.colors["text"], corner_radius=5)
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.send_button = ctk.CTkButton(self.message_frame, text="Send", command=master.send_message, fg_color=self.colors["button"], text_color=self.colors["button_text"], corner_radius=5)
        self.send_button.grid(row=0, column=1, padx=5, pady=5)

    def display_message(self, message):
        message_label = ctk.CTkLabel(self.chat_display, text=message, anchor="w", justify="left", text_color=self.colors["text"], fg_color=self.colors["secondary"], corner_radius=5, padx=10, pady=5)
        message_label.pack(fill="x", padx=5, pady=2)
