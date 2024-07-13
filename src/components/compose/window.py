# src/components/compose/window.py

import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter as ctk


class ComposeWindow(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Compose New Message")
        self.geometry("700x800")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        padding = 20
        entry_height = 35

        self.subject_label = ctk.CTkLabel(self, text="Subject:", anchor="w")
        self.subject_label.grid(
            row=0, column=0, padx=padding, pady=(padding, 5), sticky="ew"
        )
        self.subject_entry = ctk.CTkEntry(self, height=entry_height)
        self.subject_entry.grid(
            row=1, column=0, padx=padding, pady=(0, padding), sticky="ew"
        )

        recipients_frame = ctk.CTkFrame(self)
        recipients_frame.grid(
            row=2, column=0, padx=padding, pady=(0, padding), sticky="ew"
        )
        recipients_frame.grid_columnconfigure(1, weight=1)

        self.to_label = ctk.CTkLabel(recipients_frame, text="To:", anchor="w", width=30)
        self.to_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.to_entry = ctk.CTkEntry(recipients_frame, height=entry_height)
        self.to_entry.grid(row=0, column=1, pady=5, sticky="ew")

        self.cc_label = ctk.CTkLabel(recipients_frame, text="CC:", anchor="w", width=30)
        self.cc_label.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")
        self.cc_entry = ctk.CTkEntry(recipients_frame, height=entry_height)
        self.cc_entry.grid(row=1, column=1, pady=5, sticky="ew")

        self.message_label = ctk.CTkLabel(self, text="Message:", anchor="w")
        self.message_label.grid(row=3, column=0, padx=padding, pady=(0, 5), sticky="w")
        self.message_textbox = ctk.CTkTextbox(self)
        self.message_textbox.grid(
            row=4, column=0, padx=padding, pady=(0, padding), sticky="nsew"
        )

        self.advanced_options_button = ctk.CTkButton(
            self, text="Advanced Options ⌄", command=self.toggle_advanced_options
        )
        self.advanced_options_button.grid(
            row=5, column=0, padx=padding, pady=(0, padding), sticky="ew"
        )

        self.advanced_options_frame = ctk.CTkFrame(self)
        self.advanced_options_frame.grid(
            row=6, column=0, padx=padding, pady=(0, padding), sticky="ew"
        )
        self.advanced_options_frame.grid_columnconfigure(1, weight=1)
        self.advanced_options_frame.grid_remove()

        self.bcc_label = ctk.CTkLabel(
            self.advanced_options_frame, text="BCC:", anchor="w", width=30
        )
        self.bcc_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.bcc_entry = ctk.CTkEntry(self.advanced_options_frame, height=entry_height)
        self.bcc_entry.grid(row=0, column=1, pady=5, sticky="ew")

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(
            row=7, column=0, padx=padding, pady=(0, padding), sticky="ew"
        )
        self.buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        button_width = 120
        self.send_button = ctk.CTkButton(
            self.buttons_frame,
            text="Send",
            command=self.confirm_send_message,
            width=button_width,
        )
        self.send_button.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")

        self.save_button = ctk.CTkButton(
            self.buttons_frame,
            text="Save",
            command=self.confirm_save_message,
            width=button_width,
        )
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        self.cancel_button = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.confirm_cancel_message,
            fg_color="red",
            width=button_width,
        )
        self.cancel_button.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="e")

        self.advanced_options_visible = False

    def toggle_advanced_options(self) -> None:
        if self.advanced_options_visible:
            self.advanced_options_frame.grid_remove()
            self.advanced_options_button.configure(text="Advanced Options ⌄")
        else:
            self.advanced_options_frame.grid()
            self.advanced_options_button.configure(text="Advanced Options ⌃")
        self.advanced_options_visible = not self.advanced_options_visible

    def confirm_send_message(self) -> None:
        if not self.message_textbox.get("1.0", "end-1c").strip():
            messagebox.showerror("Error", "Message cannot be empty.")
            self.focus_force()
            return

        if not self.subject_entry.get().strip():
            if not messagebox.askyesno(
                "Warning", "The subject is empty. Do you want to proceed?"
            ):
                self.focus_force()
                return

        if messagebox.askyesno(
            "Confirmation", "Are you sure you want to send this message?"
        ):
            self.send_message()
        else:
            self.focus_force()

    def confirm_save_message(self) -> None:
        if not self.message_textbox.get("1.0", "end-1c").strip():
            messagebox.showerror("Error", "Message cannot be empty.")
            self.focus_force()
            return

        if not self.subject_entry.get().strip():
            if not messagebox.askyesno(
                "Warning", "The subject is empty. Do you want to proceed?"
            ):
                self.focus_force()
                return

        if messagebox.askyesno(
            "Confirmation", "Are you sure you want to save this message?"
        ):
            self.save_message()
        else:
            self.focus_force()

    def confirm_cancel_message(self) -> None:
        if messagebox.askyesno("Confirmation", "Are you sure you want to cancel?"):
            self.destroy()
        else:
            self.focus_force()

    def send_message(self) -> None:
        # Implement send message functionality here
        pass

    def save_message(self) -> None:
        # Implement save message functionality here
        pass
