import customtkinter as ctk
from typing import Any

def setup_feedback_tab(self: Any) -> None:
    feedback_frame = ctk.CTkFrame(self.feedback_tab)
    feedback_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    feedback_frame.grid_columnconfigure(0, weight=1)
    feedback_frame.grid_rowconfigure(0, weight=1)

    feedback_label = ctk.CTkLabel(
        feedback_frame,
        text="This is where the feedback goes when I've completed this part (WIP)",
        font=("Arial", 18),
        wraplength=700,
        justify="center",
    )
    feedback_label.grid(row=0, column=0, pady=20, padx=20)
