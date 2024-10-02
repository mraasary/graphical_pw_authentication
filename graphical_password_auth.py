import tkinter as tk
from tkinter import messagebox


class AuthenticatedPage(tk.Frame):
    def __init__(self, parent, username, on_submit):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.on_submit = on_submit

        # Load and display the background image
        self.photo = tk.PhotoImage(file="background.gif")
        self.background_label = tk.Label(self, image=self.photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Display the "Login Successful!" label
        self.login_successful_label = tk.Label(
            self, text="Login Successful!", font=("Helvetica", 36), fg="green")
        self.login_successful_label.pack(expand=True)

        # Display the welcome message with username
        self.welcome_label = tk.Label(
            self, text=f"Welcome, {username}!", font=("Helvetica", 24))
        self.welcome_label.pack(expand=True)

        # Display the continue message
        self.continue_label = tk.Label(
            self, text="Authentication done, continue", font=("Helvetica", 24))
        self.continue_label.pack(expand=True)

        # Generate specific form fields
        self.generate_specific_form()

    def generate_specific_form(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Styling for the form
        label_style = {"font": ("Helvetica", 16),
                       "fg": "white", "bg": "#333333"}
        entry_style = {"font": ("Helvetica", 16)}

        # Labels and Entry fields for Name, USN, and Contact Number
        tk.Label(self, text="Name:", **label_style).pack()
        self.name_entry = tk.Entry(self, **entry_style)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="USN:", **label_style).pack()
        self.usn_entry = tk.Entry(self, **entry_style)
        self.usn_entry.pack(pady=5)

        tk.Label(self, text="Contact Number:", **label_style).pack()
        self.contact_entry = tk.Entry(self, **entry_style)
        self.contact_entry.pack(pady=5)

        # Add a submit button with colorful styling
        tk.Button(self, text="Submit", font=("Helvetica", 16),
                  command=self.submit_form, bg="#4CAF50", fg="white").pack(pady=10)

    def submit_form(self):
        name = self.name_entry.get()
        usn = self.usn_entry.get()
        contact = self.contact_entry.get()

        # Validate form fields
        if not name or not usn or not contact:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Call the on_submit callback with the form data
        self.on_submit(name, usn, contact)


class GraphicalPasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphical Password Authentication System")

        self.password = []  # To store the graphical password
        self.saved_password = []  # To store the saved graphical password
        self.tolerance = 10  # Tolerance for matching points

        self.create_login_page()

    def create_login_page(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        self.canvas = tk.Canvas(self.login_frame, width=600, height=600)
        self.canvas.pack()

        self.load_background_image()

        # Add welcome message
        tk.Label(self.login_frame, text="Welcome to Graphical Password Authentication App", font=(
            "Helvetica", 24)).pack(pady=20)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Add colorful styling to buttons
        self.save_button = tk.Button(
            self.login_frame, text="Save Password", command=self.save_password, bg="#FF0000", fg="white")
        self.save_button.pack(pady=5)

        self.login_button = tk.Button(
            self.login_frame, text="Login", command=self.login, bg="#4CAF50", fg="white")
        self.login_button.pack(pady=5)

    def load_background_image(self):
        try:
            self.photo = tk.PhotoImage(file="background.gif")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        except tk.TclError:
            messagebox.showerror("Error", "Failed to load background.gif")
            self.root.destroy()

    def create_authenticated_page(self):
        self.login_frame.destroy()
        self.authenticated_page = AuthenticatedPage(
            self.root, "User", self.submit_details)
        self.authenticated_page.pack(expand=True, fill=tk.BOTH)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.password.append((x, y))
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")

    def save_password(self):
        if not self.password:
            messagebox.showerror(
                "Error", "Please select points for your password.")
            return

        self.saved_password = self.password.copy()
        messagebox.showinfo("Info", "Password saved successfully!")
        self.clear_canvas()

    def login(self):
        if not self.saved_password:
            messagebox.showerror(
                "Error", "No password saved, please save a password first!")
            return

        if self.is_password_match(self.saved_password, self.password):
            messagebox.showinfo("Info", "Login successful!")
            self.create_authenticated_page()
        else:
            messagebox.showerror("Error", "Incorrect password!")
            self.clear_canvas()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.load_background_image()
        self.password.clear()

    def is_password_match(self, saved_password, entered_password):
        if len(saved_password) != len(entered_password):
            return False

        for (sx, sy), (ex, ey) in zip(saved_password, entered_password):
            if abs(sx - ex) > self.tolerance or abs(sy - ey) > self.tolerance:
                return False
        return True

    def submit_details(self, name, usn, contact):
        # Placeholder for submitting details
        messagebox.showinfo("Details Submitted",
                            "Details submitted successfully!")
        self.show_verified_authentication()

    def show_verified_authentication(self):
        # Clear existing widgets
        for widget in self.authenticated_page.winfo_children():
            widget.destroy()

        # Display verified authentication message with colorful styling
        tk.Label(self.authenticated_page, text="Verified Authentication Done!!", font=(
            "Helvetica", 30), fg="#4CAF50").pack(pady=50)


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicalPasswordApp(root)
    root.mainloop()
