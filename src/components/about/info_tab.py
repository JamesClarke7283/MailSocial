from importlib import metadata
import customtkinter as ctk
from PIL import Image, ImageOps
from typing import Any

def setup_info_tab(self: Any) -> None:
    info_frame = ctk.CTkScrollableFrame(self.info_tab)
    info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    info_frame.grid_columnconfigure(0, weight=1)

    self.logo_path = "assets/logo.webp"
    self.dark_image = Image.open(self.logo_path)
    r, g, b, a = self.dark_image.split()
    inverted_image = ImageOps.invert(Image.merge("RGB", (r, g, b)))
    self.light_image = Image.merge(
        "RGBA",
        (
            inverted_image.split()[0],
            inverted_image.split()[1],
            inverted_image.split()[2],
            a,
        ),
    )

    self.logo_image = ctk.CTkImage(
        light_image=self.light_image, dark_image=self.dark_image, size=(200, 200)
    )
    self.logo_label = ctk.CTkLabel(info_frame, image=self.logo_image, text="")
    self.logo_label.grid(row=0, column=0, pady=(20, 10))

    self.program_name_label = ctk.CTkLabel(
        info_frame,
        text=f"Program Name: {metadata.metadata('mailsocial')['Name']}",
        font=("Arial", 24, "bold"),
    )
    self.program_name_label.grid(row=1, column=0, pady=(20, 10))

    self.version_label = ctk.CTkLabel(
        info_frame,
        text=f"Program Version: {metadata.metadata('mailsocial')['Version']}",
        font=("Arial", 20),
    )
    self.version_label.grid(row=2, column=0, pady=(5, 5))

    self.authors_label = ctk.CTkLabel(
        info_frame, text="Contributors:", font=("Arial", 20, "bold")
    )
    self.authors_label.grid(row=3, column=0, pady=(20, 10))

    contributors = self.get_contributors()

    for i, contributor in enumerate(contributors):
        contributor_frame = ctk.CTkFrame(info_frame)
        contributor_frame.grid(row=4 + i, column=0, pady=(0, 10), padx=20, sticky="ew")
        contributor_frame.grid_columnconfigure(1, weight=1)

        name_label = ctk.CTkLabel(
            contributor_frame, text=contributor["name"], font=("Arial", 16, "bold")
        )
        name_label.grid(row=0, column=0, padx=(10, 20), pady=5)

        rank_label = ctk.CTkLabel(
            contributor_frame, text=contributor["rank"], font=("Arial", 14)
        )
        rank_label.grid(row=0, column=1, padx=10, pady=5)

        email_label = ctk.CTkLabel(
            contributor_frame, text=contributor["emails"][0], font=("Arial", 14)
        )
        email_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    self.description_label = ctk.CTkLabel(
        info_frame,
        text=f"Description: {metadata.metadata('mailsocial')['Summary']}",
        font=("Arial", 18),
        wraplength=700,
        justify="center",
    )
    self.description_label.grid(row=4 + len(contributors), column=0, pady=(20, 20))