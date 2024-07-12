import customtkinter as ctk
from PIL import Image, ImageOps
from src.components.about_window import AboutWindow

class UtilityBar(ctk.CTkFrame):
    def __init__(self, master, colors, settings_command, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = colors
        self.configure(fg_color=self.colors["primary"], corner_radius=10)

        # Load the logo and create a light and dark version
        logo_path = "assets/logo.webp"
        dark_image = Image.open(logo_path).resize((64, 64))

        # Separate alpha channel
        r, g, b, a = dark_image.split()
        # Invert RGB channels
        inverted_image = ImageOps.invert(Image.merge('RGB', (r, g, b)))
        # Recombine with alpha channel
        light_image = Image.merge('RGBA', (inverted_image.split()[0], inverted_image.split()[1], inverted_image.split()[2], a))

        self.logo_image = ctk.CTkImage(light_image=light_image, dark_image=dark_image, size=(64, 64))

        # Logo button (acts like a button but looks like an image)
        self.logo_button = ctk.CTkButton(self, image=self.logo_image, text="", fg_color=self.colors["primary"], hover_color=self.colors["primary"], command=self.open_about)
        self.logo_button.pack(side="left", padx=5, pady=5)

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
