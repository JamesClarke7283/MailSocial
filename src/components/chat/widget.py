import customtkinter as ctk
from src.components.chat.messages import ChatMessages
from src.components.chat.input import MessageInput
from src.core.models.chat import Chat

class ChatInterface(ctk.CTkFrame):
    def __init__(self, master, colors, *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)
        self.colors = colors
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.chat_display = ChatMessages(self, colors=self.colors)
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.message_frame = MessageInput(self, colors=self.colors, send_command=master.send_message)
        self.message_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

    def display_message(self, message, sender="You", is_user=True):
        self.chat_display.display_message(message, sender, is_user)

    def update_colors(self, colors):
        self.colors = colors
        self.chat_display.update_colors(colors)
        self.message_frame.update_colors(colors)

    def display_chat(self, chat: Chat):
        self.chat_display.clear_messages()
        for message in chat.messages:
            sender = message.sender.name if message.sender.name else message.sender.email
            is_user = sender == "You"
            self.chat_display.display_message(message.content, sender, is_user)
