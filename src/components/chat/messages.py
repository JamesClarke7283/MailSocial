import customtkinter as ctk

class ChatMessages(ctk.CTkFrame):
    def __init__(self, master, colors, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.configure(fg_color=self.colors["secondary"], corner_radius=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def display_message(self, message):
        message_label = ctk.CTkLabel(self, text=message, anchor="w", justify="left", text_color=self.colors["text"], fg_color=self.colors["secondary"], corner_radius=5, padx=10, pady=5)
        message_label.pack(fill="x", padx=5, pady=2)
