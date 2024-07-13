import customtkinter as ctk
from typing import Any


def setup_licenses_tab(self: Any) -> None:
    licenses_frame = ctk.CTkFrame(self.licenses_tab)
    licenses_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    licenses_frame.grid_columnconfigure(0, weight=1)
    licenses_frame.grid_rowconfigure(1, weight=1)

    self.license_type_var = ctk.StringVar(value="Code")
    self.license_type_dropdown = ctk.CTkOptionMenu(
        licenses_frame,
        values=["Code", "Assets", "Documentation"],
        variable=self.license_type_var,
        command=self.update_license_text,
    )
    self.license_type_dropdown.grid(
        row=0, column=0, pady=(20, 10), padx=20, sticky="ew"
    )

    self.license_text = ctk.CTkTextbox(licenses_frame, wrap="word", state="disabled")
    self.license_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

    self.update_license_text()


def update_license_text(self: Any, *args: Any) -> None:
    license_type = self.license_type_var.get()
    file_path = {
        "Code": "LICENSE.md",
        "Documentation": "docs/LICENSE.md",
        "Assets": "assets/LICENSE",
    }.get(license_type)

    try:
        with open(file_path or "", "r") as f:
            license_content = f.read()
    except FileNotFoundError:
        license_content = f"License file for {license_type} not found."

    self.license_text.configure(state="normal")
    self.license_text.delete("1.0", ctk.END)
    self.license_text.insert("1.0", license_content)
    self.license_text.configure(state="disabled")
