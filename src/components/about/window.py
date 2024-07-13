import customtkinter as ctk
from PIL import Image, ImageOps
from typing import List, Dict, Any
from .contributors import get_contributors
from .feedback_tab import setup_feedback_tab
from .info_tab import setup_info_tab
from .licenses_tab import setup_licenses_tab, update_license_text

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.title("About")
        self.geometry("800x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.info_tab = self.tabview.add("Info")
        self.licenses_tab = self.tabview.add("Licenses")
        self.feedback_tab = self.tabview.add("Feedback")

        for tab in [self.info_tab, self.licenses_tab, self.feedback_tab]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

        self.setup_info_tab()
        self.setup_licenses_tab()
        self.setup_feedback_tab()

        self.bind("<Configure>", self.adjust_logo_size)

    def setup_info_tab(self) -> None:
        setup_info_tab(self)

    def setup_licenses_tab(self) -> None:
        setup_licenses_tab(self)

    def setup_feedback_tab(self) -> None:
        setup_feedback_tab(self)

    def get_contributors(self) -> List[Dict[str, Any]]:
        return get_contributors()

    def update_license_text(self, *args: Any) -> None:
        update_license_text(self, *args)

    def adjust_logo_size(self, event: Any = None) -> None:
        current_height = self.winfo_height()
        new_height = int(current_height * 0.33)
        new_width = int(
            self.dark_image.size[0] * (new_height / self.dark_image.size[1])
        )

        self.dark_image_resized = self.dark_image.resize(
            (new_width, new_height), Image.LANCZOS
        )
        self.light_image_resized = self.light_image.resize(
            (new_width, new_height), Image.LANCZOS
        )

        self.logo_image = ctk.CTkImage(
            light_image=self.light_image_resized,
            dark_image=self.dark_image_resized,
            size=(new_width, new_height),
        )
        self.logo_label.configure(image=self.logo_image)
