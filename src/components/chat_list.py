import customtkinter as ctk
import tkinter as tk

class ChatList(ctk.CTkFrame):
    def __init__(self, master, colors, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.configure(fg_color=self.colors["primary"], corner_radius=10)

        self.chat_listbox = tk.Listbox(self, bg=self.colors["primary"], fg=self.colors["text"], selectbackground="gray50", highlightthickness=1, highlightcolor=self.colors["border"], relief="flat")
        self.chat_listbox.pack(fill="both", expand=True, padx=5, pady=5)
