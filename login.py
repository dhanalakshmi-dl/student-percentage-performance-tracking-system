import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3


class LoginPage:

    def __init__(self, root):

        self.root = root
        self.root.title("College Performance System")
        self.root.geometry("900x600")

        # ===== BACKGROUND IMAGE =====
        bg = Image.open("assets/background.jpg")
        bg = bg.resize((900, 600))
        self.bg_img = ImageTk.PhotoImage(bg)

        bg_label = tk.Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ===== LOGIN BOX =====
        frame = tk.Frame(self.root, bg="white", bd=3)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=360, height=420)

        # ===== COLLEGE LOGO =====
        logo = Image.open("assets/logo.png")
        logo = logo.resize((80, 80))
        self.logo_img = ImageTk.PhotoImage(logo)

        tk.Label(frame, image=self.logo_img, bg="white").pack(pady=10)

        # ===== COLLEGE NAME =====
        tk.Label(
            frame,
            text="NEHRU MEMORIAL COLLEGE",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="darkblue",
            justify="center",
            wraplength=260
        ).pack(pady=5)

        # ===== PROJECT TITLE =====
        tk.Label(
            frame,
            text="Student Performance Analysis System",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        ).pack(pady=2)

        # ===== USERNAME =====
        tk.Label(frame, text="Username", bg="white").pack(pady=5)
        self.username_entry = tk.Entry(frame)
        self.username_entry.pack()

        # ===== PASSWORD =====
        tk.Label(frame, text="Password", bg="white").pack(pady=5)
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack()

        # ===== ROLE =====
        tk.Label(frame, text="Login As", bg="white").pack(pady=5)

        self.role_combo = ttk.Combobox(
            frame,
            values=["Admin", "Staff", "Student"],
            state="readonly"
        )
        self.role_combo.pack()

        # ===== LOGIN BUTTON =====
        tk.Button(
            frame,
            text="Login",
            bg="royalblue",
            fg="white",
            width=15,
            command=self.login
        ).pack(pady=20)

    # ===== LOGIN FUNCTION =====
    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combo.get()

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role=?",
            (username, password, role)
        )

        result = cursor.fetchone()

        conn.close()

        if result:

            messagebox.showinfo("Success", "Login Successful")

            if role == "Admin":
                from admin_dashboard import AdminDashboard
                new = tk.Toplevel(self.root)
                AdminDashboard(new)

            elif role == "Staff":
                from staff_dashboard import StaffDashboard
                new = tk.Toplevel(self.root)
                StaffDashboard(new)

            elif role == "Student":
                from student_dashboard import StudentDashboard
                new = tk.Toplevel(self.root)
                StudentDashboard(new)

        else:
            messagebox.showerror("Error", "Invalid Login Details")


# ===== MAIN =====
if __name__ == "__main__":

    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()
