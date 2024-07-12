import customtkinter as ctk
from importlib import metadata
from PIL import Image, ImageOps
import json
import os

class ExpandableEmailFrame(ctk.CTkFrame):
    def __init__(self, master, emails, **kwargs):
        super().__init__(master, **kwargs)
        self.emails = emails
        self.expanded = False
        
        self.main_email = max(emails, key=emails.get)
        self.main_label = ctk.CTkLabel(self, text=self.main_email, anchor="e", justify="right")
        self.main_label.pack(side="right", padx=(0, 10))
        
        self.expand_button = ctk.CTkButton(self, text="▼", width=20, command=self.toggle_expand)
        self.expand_button.pack(side="right")
        
        self.email_labels = []

    def toggle_expand(self):
        if self.expanded:
            for label in self.email_labels:
                label.pack_forget()
            self.expand_button.configure(text="▼")
        else:
            sorted_emails = sorted(self.emails.items(), key=lambda x: x[1], reverse=True)
            for email, percentage in sorted_emails:
                if email != self.main_email:
                    label = ctk.CTkLabel(self, text=f"{email} ({percentage:.2f}%)", anchor="e", justify="right")
                    label.pack(side="bottom", padx=(0, 10))
                    self.email_labels.append(label)
            self.expand_button.configure(text="▲")
        self.expanded = not self.expanded

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent):
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

    def setup_info_tab(self):
        info_frame = ctk.CTkScrollableFrame(self.info_tab)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        info_frame.grid_columnconfigure(0, weight=1)

        self.logo_path = "assets/logo.webp"
        self.dark_image = Image.open(self.logo_path)
        r, g, b, a = self.dark_image.split()
        inverted_image = ImageOps.invert(Image.merge('RGB', (r, g, b)))
        self.light_image = Image.merge('RGBA', (inverted_image.split()[0], inverted_image.split()[1], inverted_image.split()[2], a))

        self.logo_image = ctk.CTkImage(light_image=self.light_image, dark_image=self.dark_image, size=(200, 200))
        self.logo_label = ctk.CTkLabel(info_frame, image=self.logo_image, text="")
        self.logo_label.grid(row=0, column=0, pady=(20, 10))

        self.program_name_label = ctk.CTkLabel(info_frame, text=f"Program Name: {metadata.metadata('mailsocial')['Name']}", font=("Arial", 24, "bold"))
        self.program_name_label.grid(row=1, column=0, pady=(20, 10))

        self.version_label = ctk.CTkLabel(info_frame, text=f"Program Version: {metadata.metadata('mailsocial')['Version']}", font=("Arial", 20))
        self.version_label.grid(row=2, column=0, pady=(5, 5))

        self.authors_label = ctk.CTkLabel(info_frame, text="Contributors:", font=("Arial", 20, "bold"))
        self.authors_label.grid(row=3, column=0, pady=(20, 10))

        self.explanation_label = ctk.CTkLabel(info_frame, text="To prevent people from spoofing identities, contributors must have a full name and email listed on their public GitHub profile. Verified contributors are listed below.", font=("Arial", 16), wraplength=700, justify="left")
        self.explanation_label.grid(row=4, column=0, pady=(10, 10))

        self.verified_label = ctk.CTkLabel(info_frame, text="Verified Contributors:", font=("Arial", 18, "bold"))
        self.verified_label.grid(row=5, column=0, pady=(10, 10))

        verified_contributors, unverified_contributors = self.get_contributors()

        for i, contributor in enumerate(verified_contributors):
            contributor_frame = ctk.CTkFrame(info_frame)
            contributor_frame.grid(row=6+i, column=0, pady=(0, 10), padx=20, sticky="ew")
            contributor_frame.grid_columnconfigure(1, weight=1)

            name_label = ctk.CTkLabel(contributor_frame, text=contributor['name'], font=("Arial", 16, "bold"))
            name_label.grid(row=0, column=0, padx=(10, 20), pady=5)

            rank_label = ctk.CTkLabel(contributor_frame, text=contributor['rank'], font=("Arial", 14))
            rank_label.grid(row=0, column=1, padx=10, pady=5)

            email_frame = ExpandableEmailFrame(contributor_frame, contributor['emails'])
            email_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        self.unverified_label = ctk.CTkLabel(info_frame, text="Unverified Contributors:", font=("Arial", 18, "bold"))
        self.unverified_label.grid(row=6+len(verified_contributors), column=0, pady=(10, 10))

        for i, contributor in enumerate(unverified_contributors):
            contributor_frame = ctk.CTkFrame(info_frame)
            contributor_frame.grid(row=7+len(verified_contributors)+i, column=0, pady=(0, 10), padx=20, sticky="ew")
            contributor_frame.grid_columnconfigure(1, weight=1)

            name_label = ctk.CTkLabel(contributor_frame, text=contributor['name'], font=("Arial", 16, "bold"))
            name_label.grid(row=0, column=0, padx=(10, 20), pady=5)

            rank_label = ctk.CTkLabel(contributor_frame, text=contributor['rank'], font=("Arial", 14))
            rank_label.grid(row=0, column=1, padx=10, pady=5)

            email_frame = ExpandableEmailFrame(contributor_frame, contributor['emails'])
            email_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        self.description_label = ctk.CTkLabel(info_frame, text=f"Description: {metadata.metadata('mailsocial')['Summary']}", font=("Arial", 18), wraplength=700, justify="center")
        self.description_label.grid(row=7+len(verified_contributors)+len(unverified_contributors), column=0, pady=(20, 20))

    def get_contributors(self):
        credits_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.credits.json')
        try:
            with open(credits_file, 'r') as f:
                credits_data = json.load(f)
        except FileNotFoundError:
            print(f"Credits file not found: {credits_file}")
            return [], []

        verified_contributors = []
        unverified_contributors = []

        for user_id, data in credits_data.items():
            rank = self.calculate_rank(data['total_contribution_percentage'])
            contributor = {
                'name': user_id,
                'emails': {identity['email']: identity['contribution_percentage'] for identity in data['identities']},
                'rank': rank,
                'total_contribution': data['total_contribution_percentage']
            }
            if data['verified']:
                verified_contributors.append(contributor)
            else:
                unverified_contributors.append(contributor)

        # Sort contributors by total contribution percentage in descending order
        verified_contributors.sort(key=lambda x: x['total_contribution'], reverse=True)
        unverified_contributors.sort(key=lambda x: x['total_contribution'], reverse=True)

        return verified_contributors, unverified_contributors

    def calculate_rank(self, percentage):
        if percentage < 1:
            return "Newbie"
        elif percentage < 5:
            return "Amateur"
        elif percentage < 10:
            return "Contributor"
        elif percentage < 25:
            return "Co-Maintainer"
        elif percentage < 50:
            return "Maintainer"
        else:
            return "Lead Maintainer"

    def setup_licenses_tab(self):
        licenses_frame = ctk.CTkFrame(self.licenses_tab)
        licenses_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        licenses_frame.grid_columnconfigure(0, weight=1)
        licenses_frame.grid_rowconfigure(1, weight=1)

        self.license_type_var = ctk.StringVar(value="Code")
        self.license_type_dropdown = ctk.CTkOptionMenu(
            licenses_frame,
            values=["Code", "Assets", "Documentation"],
            variable=self.license_type_var,
            command=self.update_license_text
        )
        self.license_type_dropdown.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.license_text = ctk.CTkTextbox(licenses_frame, wrap="word", state="disabled")
        self.license_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.update_license_text()

    def setup_feedback_tab(self):
        feedback_frame = ctk.CTkFrame(self.feedback_tab)
        feedback_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        feedback_frame.grid_columnconfigure(0, weight=1)
        feedback_frame.grid_rowconfigure(0, weight=1)

        feedback_label = ctk.CTkLabel(feedback_frame, text="This is where the feedback goes when I've completed this part (WIP)", font=("Arial", 18), wraplength=700, justify="center")
        feedback_label.grid(row=0, column=0, pady=20, padx=20)

    def update_license_text(self, *args):
        license_type = self.license_type_var.get()
        file_path = {
            "Code": "LICENSE.md",
            "Documentation": "docs/LICENSE.md",
            "Assets": "assets/LICENSE"
        }.get(license_type)

        try:
            with open(file_path, "r") as f:
                license_content = f.read()
        except FileNotFoundError:
            license_content = f"License file for {license_type} not found."

        self.license_text.configure(state="normal")
        self.license_text.delete("1.0", ctk.END)
        self.license_text.insert("1.0", license_content)
        self.license_text.configure(state="disabled")

    def adjust_logo_size(self, event=None):
        current_height = self.winfo_height()
        new_height = int(current_height * 0.25)
        new_width = int(self.dark_image.size[0] * (new_height / self.dark_image.size[1]))

        self.dark_image_resized = self.dark_image.resize((new_width, new_height), Image.LANCZOS)
        self.light_image_resized = self.light_image.resize((new_width, new_height), Image.LANCZOS)

        self.logo_image = ctk.CTkImage(light_image=self.light_image_resized, dark_image=self.dark_image_resized, size=(new_width, new_height))
        self.logo_label.configure(image=self.logo_image)
