import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFont

class ChatItem(ctk.CTkFrame):
    def __init__(self, master, colors, name, message, font_size, *args, **kwargs):
        super().__init__(master, fg_color=colors["secondary"], *args, **kwargs)
        self.colors = colors
        self.font_size = font_size.get()  # Get the actual integer value

        # Create circular image
        size = int(self.font_size * 2.5)  # Adjust image size based on font size
        image = Image.new('RGB', (size, size), self.colors["button"])
        draw = ImageDraw.Draw(image)
        draw.ellipse([0, 0, size, size], fill=self.colors["button"])
        
        # Use a proper PIL ImageFont
        try:
            font = ImageFont.truetype("arial.ttf", int(self.font_size * 1.2))
        except IOError:
            font = ImageFont.load_default()

        draw.text((size/2, size/2), name[0].upper(), fill=self.colors["button_text"], anchor='mm', font=font)
        photo = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self, image=photo, bg=self.colors["secondary"])
        self.image_label.image = photo
        self.image_label.pack(side="left", padx=(10, 5), pady=10)

        self.text_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.text_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        self.name_label = ctk.CTkLabel(self.text_frame, text=name, anchor="w", font=("Arial", int(self.font_size * 1.2), "bold"))
        self.name_label.pack(side="top", fill="x")

        self.message_label = ctk.CTkLabel(self.text_frame, text=self.truncate_message(message), anchor="w", font=("Arial", self.font_size))
        self.message_label.pack(side="top", fill="x")

    def truncate_message(self, message):
        max_chars = int(200 / self.font_size * 10)  # Adjust based on font size
        return message[:max_chars] + "..." if len(message) > max_chars else message

    def update_font_size(self, new_size):
        self.font_size = new_size
        self.name_label.configure(font=("Arial", int(self.font_size * 1.2), "bold"))
        self.message_label.configure(font=("Arial", self.font_size), text=self.truncate_message(self.message_label.cget("text")))

class ChatList(ctk.CTkScrollableFrame):
    def __init__(self, master, colors, font_size, *args, **kwargs):
        super().__init__(master, fg_color=colors["primary"], *args, **kwargs)
        self.colors = colors
        self.font_size = font_size

        self.chat_items = []

        sample_chats = [
            ("General", "Welcome to the general chat!"),
            ("Work", "Don't forget the meeting at 2 PM"),
            ("Family", "Mom: Are you coming for dinner?"),
            ("Friends", "Hey, want to grab coffee later?")
        ]

        for name, message in sample_chats:
            chat_item = ChatItem(self, self.colors, name, message, self.font_size)
            chat_item.pack(fill="x", padx=5, pady=2)
            self.chat_items.append(chat_item)

    def update_font_size(self, new_size):
        for chat_item in self.chat_items:
            chat_item.update_font_size(new_size)