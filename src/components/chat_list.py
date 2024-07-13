import tkinter as tk
from datetime import datetime

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk

from src.core.models.chat import Chat
from src.core.models.member import Member
from src.core.models.message import Message, MessageStatus


class ChatItem(ctk.CTkButton):
    def __init__(self, master, chat, font_size, app_instance, *args, **kwargs):
        super().__init__(master, fg_color=master.colors["secondary"], *args, **kwargs)
        self.chat = chat
        self.font_size = font_size.get()
        self.colors = master.colors
        self.app_instance = app_instance

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Create circular image
        size = int(self.font_size * 2.5)
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, size, size), fill=self.colors["button"])

        # Use a proper PIL ImageFont
        try:
            font = ImageFont.truetype("arial.ttf", int(self.font_size * 1.2))
        except IOError:
            font = ImageFont.load_default()

        draw.text(
            (size / 2, size / 2),
            chat.title[0].upper(),
            fill=self.colors["button_text"],
            anchor="mm",
            font=font,
        )
        photo = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self, image=photo, bg=self.colors["secondary"])
        self.image_label.image = photo
        self.image_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.text_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.text_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        self.name_label = ctk.CTkLabel(
            self.text_frame,
            text=chat.title,
            anchor="w",
            font=("Arial", int(self.font_size * 1.2), "bold"),
        )
        self.name_label.grid(row=0, column=0, sticky="w")

        self.message_label = ctk.CTkLabel(
            self.text_frame,
            text=self.truncate_message(chat.messages[-1].content),
            anchor="w",
            font=("Arial", self.font_size),
        )
        self.message_label.grid(row=1, column=0, sticky="w")

        self.configure(command=self.on_click)

    def truncate_message(self, message):
        max_chars = int(200 / self.font_size * 10)
        return message[:max_chars] + "..." if len(message) > max_chars else message

    def update_font_size(self, new_size):
        self.font_size = new_size
        self.name_label.configure(font=("Arial", int(self.font_size * 1.2), "bold"))
        self.message_label.configure(
            font=("Arial", self.font_size),
            text=self.truncate_message(self.chat.messages[-1].content),
        )

    def update_colors(self, colors):
        self.colors = colors
        self.configure(fg_color=colors["secondary"])
        self.image_label.configure(bg=colors["secondary"])
        size = int(self.font_size * 2.5)
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, size, size), fill=colors["button"])
        try:
            font = ImageFont.truetype("arial.ttf", int(self.font_size * 1.2))
        except IOError:
            font = ImageFont.load_default()
        draw.text(
            (size / 2, size / 2),
            self.chat.title[0].upper(),
            fill=colors["button_text"],
            anchor="mm",
            font=font,
        )
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        self.name_label.configure(text_color=colors["text"])
        self.message_label.configure(text_color=colors["text"])

    def on_click(self):
        self.app_instance.display_chat(self.chat)


class ChatList(ctk.CTkScrollableFrame):
    def __init__(self, master, colors, font_size, app_instance, *args, **kwargs):
        super().__init__(master, fg_color=colors["primary"], *args, **kwargs)
        self.colors = colors
        self.font_size = font_size
        self.chat_items = []
        self.app_instance = app_instance

        self.compose_button = ctk.CTkButton(
            self,
            text="📝 Compose",
            command=self.app_instance.open_compose_window,
            fg_color=self.colors["button"],
            text_color=self.colors["button_text"],
            corner_radius=5,
        )
        self.compose_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        sample_chats = [
            Chat(
                "General",
                [Member("general@example.com", "123", True, "General")],
                [
                    Message(
                        [],
                        Member("general@example.com", "123", True, "General"),
                        "Welcome to the general chat!",
                        datetime.now(),
                        MessageStatus.DRAFT,
                    ),
                    Message(
                        [],
                        Member("johndoe@example.com", "456", True, "John Doe"),
                        "Got it, thanks!",
                        datetime.now(),
                        MessageStatus.SENT,
                    ),
                    Message(
                        [],
                        Member("me@example.com", "789", True, "You"),
                        "Hello everyone!",
                        datetime.now(),
                        MessageStatus.READ,
                    ),
                    Message(
                        [],
                        Member("unknown@example.com", "000", True, None),
                        "Who is this?",
                        datetime.now(),
                        MessageStatus.LOCAL_ONLY,
                    ),
                ],
            ),
            Chat(
                "Work",
                [Member("work@example.com", "123", True, "Work")],
                [
                    Message(
                        [],
                        Member("work@example.com", "123", True, "Work"),
                        "Don't forget the meeting at 2 PM",
                        datetime.now(),
                        MessageStatus.DRAFT,
                    ),
                    Message(
                        [],
                        Member("johndoe@example.com", "456", True, "John Doe"),
                        "Got it, thanks!",
                        datetime.now(),
                        MessageStatus.SENT,
                    ),
                    Message(
                        [],
                        Member("me@example.com", "789", True, "You"),
                        "I'll be there!",
                        datetime.now(),
                        MessageStatus.READ,
                    ),
                ],
            ),
            Chat(
                "Family",
                [Member("family@example.com", "123", True, "Family")],
                [
                    Message(
                        [],
                        Member("mom@example.com", "123", True, "Mom"),
                        "Are you coming for dinner?",
                        datetime.now(),
                        MessageStatus.DRAFT,
                    ),
                    Message(
                        [],
                        Member("me@example.com", "789", True, "You"),
                        "Yes, I'll be there at 7 PM.",
                        datetime.now(),
                        MessageStatus.SENT,
                    ),
                ],
            ),
            Chat(
                "Friends",
                [Member("friends@example.com", "123", True, "Friends")],
                [
                    Message(
                        [],
                        Member("friend@example.com", "123", True, "Friend"),
                        "Hey, want to grab coffee later?",
                        datetime.now(),
                        MessageStatus.DRAFT,
                    ),
                    Message(
                        [],
                        Member("me@example.com", "789", True, "You"),
                        "Sure, see you at 5!",
                        datetime.now(),
                        MessageStatus.SENT,
                    ),
                ],
            ),
        ]

        for chat in sample_chats:
            chat_item = ChatItem(self, chat, self.font_size, self.app_instance)
            chat_item.grid(
                row=len(self.chat_items) + 1, column=0, sticky="ew", padx=5, pady=2
            )
            self.chat_items.append(chat_item)

    def update_font_size(self, new_size):
        for chat_item in self.chat_items:
            chat_item.update_font_size(new_size)

    def update_colors(self, colors):
        self.colors = colors
        self.configure(fg_color=self.colors["primary"])
        for chat_item in self.chat_items:
            chat_item.update_colors(colors)
