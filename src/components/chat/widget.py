# ./src/components/chat/widget.py
import customtkinter as ctk
from src.components.chat.messages import ChatMessages
from src.components.chat.input import MessageInput

class ChatInterface(ctk.CTkFrame):
    def __init__(self, master, colors, *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)
        self.colors = colors

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Chat display area
        self.chat_display = ChatMessages(self, colors=self.colors)
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Message input area
        self.message_frame = MessageInput(self, colors=self.colors, send_command=master.send_message)
        self.message_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

    def display_message(self, message):
        self.chat_display.display_message(message)

    def update_colors(self, colors):
        self.colors = colors
        self.chat_display.update_colors(colors)
        self.message_frame.update_colors(colors)
