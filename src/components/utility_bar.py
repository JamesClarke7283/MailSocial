# ./src/components/utility_bar.py
import customtkinter as ctk
from src.components.about.window import AboutWindow

class UtilityBar(ctk.CTkFrame):
    def __init__(self, master, colors, settings_command, *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)
        self.colors = colors

        button_size = 40

        # Information button
        self.info_button = ctk.CTkButton(self, text="❔", command=self.open_about, 
                                         fg_color=self.colors["button"], 
                                         text_color=self.colors["button_text"], 
                                         corner_radius=5, width=button_size, height=button_size)
        self.info_button.pack(side="left", padx=(0, 5))

        # Settings button (cog icon)
        self.settings_button = ctk.CTkButton(self, text="⚙", command=settings_command, 
                                             fg_color=self.colors["button"], 
                                             text_color=self.colors["button_text"], 
                                             corner_radius=5, width=button_size, height=button_size)
        self.settings_button.pack(side="left", padx=5)

        # Profile button (person silhouette)
        self.profile_button = ctk.CTkButton(self, text="👤", command=self.open_profile, 
                                            fg_color=self.colors["button"], 
                                            text_color=self.colors["button_text"], 
                                            corner_radius=5, width=button_size, height=button_size)
        self.profile_button.pack(side="left", padx=(5, 0))

    def open_about(self):
        AboutWindow(self).grab_set()

    def open_profile(self):
        print("Profile button clicked")

    def update_colors(self, colors):
        self.colors = colors
        self.info_button.configure(fg_color=self.colors["button"], text_color=self.colors["button_text"])
        self.settings_button.configure(fg_color=self.colors["button"], text_color=self.colors["button_text"])
        self.profile_button.configure(fg_color=self.colors["button"], text_color=self.colors["button_text"])
