import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from importlib import metadata

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About")
        self.geometry("600x400")

        # Create a notebook
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Info tab
        info_frame = ctk.CTkFrame(notebook)
        info_text = ctk.CTkLabel(info_frame, text=self.get_info_text(), anchor="w", justify="left", wraplength=550)
        info_text.pack(expand=True, fill="both", padx=10, pady=10)
        notebook.add(info_frame, text="Info")

        # Licenses tab
        licenses_frame = ctk.CTkFrame(notebook)
        licenses_text = ctk.CTkTextbox(licenses_frame)
        licenses_text.insert("1.0", self.get_licenses_text())
        licenses_text.configure(state="disabled")
        licenses_text.pack(expand=True, fill="both", padx=10, pady=10)
        notebook.add(licenses_frame, text="Licenses")

        # Feedback tab
        feedback_frame = ctk.CTkFrame(notebook)
        feedback_label = ctk.CTkLabel(feedback_frame, text="Feedback form will go here.", anchor="w", justify="left")
        feedback_label.pack(expand=True, fill="both", padx=10, pady=10)
        notebook.add(feedback_frame, text="Feedback")

    def get_info_text(self):
        project_name = metadata.metadata('mailsocial')['Name']
        version = metadata.metadata('mailsocial')['Version']
        description = metadata.metadata('mailsocial')['Summary']
        return f"Program Name: {project_name}\nProgram Version: {version}\nDescription: {description}"

    def get_licenses_text(self):
        licenses_text = "Code License:\n\n"
        with open("LICENSE.md", "r") as f:
            licenses_text += f.read() + "\n\n"

        licenses_text += "Documentation License:\n\n"
        with open("docs/LICENSE.md", "r") as f:
            licenses_text += f.read() + "\n\n"

        licenses_text += "Assets License:\n\n"
        with open("assets/LICENSE", "r") as f:
            licenses_text += f.read()

        return licenses_text
