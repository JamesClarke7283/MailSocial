import customtkinter as ctk
from src.components.about_window import AboutWindow

class UtilityBar(ctk.CTkFrame):
    def __init__(self, master, colors, settings_command, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.configure(fg_color=self.colors["primary"], corner_radius=10)

        # Information button
        self.info_button = ctk.CTkButton(self, text="❔", command=self.open_about, fg_color=self.colors["button"], text_color=self.colors["button_text"], corner_radius=5)
        self.info_button.pack(side="left", padx=5, pady=5)

        # Settings button (cog icon)
        self.settings_button = ctk.CTkButton(self, text="⚙", command=settings_command, fg_color=self.colors["button"], text_color=self.colors["button_text"], corner_radius=5)
        self.settings_button.pack(side="left", padx=5, pady=5)

        # Profile button (person silhouette)
        self.profile_button = ctk.CTkButton(self, text="👤", command=self.open_profile, fg_color=self.colors["button"], text_color=self.colors["button_text"], corner_radius=5)
        self.profile_button.pack(side="left", padx=5, pady=5)

    def open_about(self):
        AboutWindow(self).grab_set()

    def open_profile(self):
        print("Profile button clicked")
