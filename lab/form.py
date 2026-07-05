import re
import tkinter as tk
from tkinter import messagebox


class ValidationError(Exception):
    pass


class SafeBiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeBite - Personalized Allergy Companion")
        self.root.geometry("420x500")
        self.root.config(bg="#f4f6f9")
        self.users_db = {"simon123": "SecurePass1"}
        self.show_registration_form()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def validate_inputs(self, username, email, phone, password, allergies):
        user_pattern = re.compile(r"^[a-zA-Z0-9_]{5,15}$")
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        phone_pattern = re.compile(r"^\d{10}$")
        if not user_pattern.fullmatch(username):
            raise ValidationError("Username must be 5-15 characters (letters, numbers, underscores)")
        if not email_pattern.fullmatch(email):
            raise ValidationError("Please enter a valid email address")
        if not phone_pattern.fullmatch(phone):
            raise ValidationError("Phone number must be exactly 10 digits")
        if not re.search(r"[A-Z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[!@#$%^&*]", password):
            raise ValidationError("Password must contain an uppercase letter, a number, and a special character (!@#$%^&*).")
        if re.match(r"\s", password):
            raise ValidationError("Password cannot start with a blank space")
        allergy_list = re.split(r"[,;]\s*", allergies)
        allergy_list = [a.strip() for a in allergy_list if a.strip()]
        cleaned_allergies = []
        for allergy in allergy_list:
            if re.findall(r"[0-9!@#$%^&*]", allergy):
                raise ValidationError(f"Invalid characters are detected in allergy item: '{allergy}'")
            sanitized = re.sub(r"\s+", " ", allergy).lower()
            cleaned_allergies.append(sanitized)
        return cleaned_allergies

    def show_registration_form(self):
        self.clear_window()
        tk.Label(self.root, text="SafeBite registration", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=15)
        fields = [("Username:", "user"), ("Email:", "email"), ("Phone:", "phone"), ("Password:", "pass"), ("Allergies (comma separated):", "algo")]
        self.entries = {}
        for label_text, key in fields:
            tk.Label(self.root, text=label_text, font=("Arial", 10), bg="#f4f6f9").pack(anchor="w", padx=40)
            entry = tk.Entry(self.root, font=("Arial", 10), width=35, show="*" if key == "pass" else "")
            entry.pack(pady=4)
            self.entries[key] = entry
        tk.Button(self.root, text="Register Profile", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", bd=0, width=25, height=2, command=self.handle_registration).pack(pady=15)
        tk.Button(self.root, text="Already have an account? Login", font=("Arial", 9, "underline"), bg="#f4f6f9", fg="#3498db", bd=0, command=self.show_login_form).pack()

    def handle_registration(self):
        try:
            username = self.entries["user"].get().strip()
            email = self.entries["email"].get().strip()
            phone = self.entries["phone"].get().strip()
            password = self.entries["pass"].get()
            allergies = self.entries["algo"].get().strip()
            if not all([username, email, phone, password]):
                raise ValidationError("All main credentials fields are mandatory")
            final_allergies = self.validate_inputs(username, email, phone, password, allergies)
            if username in self.users_db:
                raise ValidationError("Username already registered")
            self.users_db[username] = password
            messagebox.showinfo("Success", f"Account created for {username}!\nAllergies Monitored: {', '.join(final_allergies)}")
            self.show_login_form()
        except ValidationError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected system issue occurred: {e}")

    def show_login_form(self):
        self.clear_window()
        tk.Label(self.root, text="SafeBite Client Login", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=30)
        tk.Label(self.root, text="Username:", font=("Arial", 10), bg="#f4f6f9").pack(anchor="w", padx=40)
        self.login_user = tk.Entry(self.root, font=("Arial", 10), width=35)
        self.login_user.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Arial", 10), bg="#f4f6f9").pack(anchor="w", padx=40)
        self.login_pass = tk.Entry(self.root, font=("Arial", 10), width=35, show="*")
        self.login_pass.pack(pady=5)
        tk.Button(self.root, text="Secure Login", font=("Arial", 11, "bold"), bg="#3498db", fg="white", bd=0, width=25, height=2, command=self.handle_login).pack(pady=25)
        tk.Button(self.root, text="New Companion? Register Here", font=("Arial", 9, "underline"), bg="#f4f6f9", fg="#2ecc71", bd=0, command=self.show_registration_form).pack()

    def handle_login(self):
        try:
            username = self.login_user.get().strip()
            password = self.login_pass.get()
            if not username or not password:
                raise ValidationError("Please fill in both fields.")
            if username in self.users_db and self.users_db[username] == password:
                messagebox.showinfo("Access Granted", f"Welcome back to SafeBite, {username}!")
            else:
                raise ValidationError("Invalid Username or Password configuration.")
        except ValidationError as ve:
            messagebox.showerror("Login Error", str(ve))

app_root = tk.Tk()
app = SafeBiteApp(app_root)
app_root.mainloop()