import customtkinter as ctk

class MessageInput(ctk.CTkFrame):
    def __init__(self, master, colors, send_command, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.configure(fg_color=self.colors["tertiary"], corner_radius=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.message_entry = ctk.CTkEntry(self, placeholder_text="Write a message...", fg_color=self.colors["primary"], text_color=self.colors["text"], corner_radius=5)
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.send_button = ctk.CTkButton(self, text="Send", command=send_command, fg_color=self.colors["button"], text_color=self.colors["button_text"], corner_radius=5)
        self.send_button.grid(row=0, column=1, padx=5, pady=5)

    def get_message(self):
        return self.message_entry.get()

    def clear_message(self):
        self.message_entry.delete(0, ctk.END)
