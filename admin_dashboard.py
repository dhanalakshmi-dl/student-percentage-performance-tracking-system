import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class AdminDashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("500x400")

        title = tk.Label(root,
                         text="ADMIN DASHBOARD",
                         font=("Arial", 20, "bold"),
                         fg="darkblue")
        title.pack(pady=20)

        # Buttons

        add_btn = tk.Button(root,
                            text="Add Student",
                            width=25,
                            height=2,
                            command=self.add_student_window)
        add_btn.pack(pady=10)

        view_btn = tk.Button(root,
                             text="View Students",
                             width=25,
                             height=2,
                             command=self.view_student_window)
        view_btn.pack(pady=10)

        merit_btn = tk.Button(root,
                              text="Top 10 Merit List",
                              width=25,
                              height=2,
                              command=self.merit_window)
        merit_btn.pack(pady=10)

        self.create_tables()

    # ------------------------
    # DATABASE
    # ------------------------

    def create_tables(self):

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
        student_id INTEGER PRIMARY KEY,
        name TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results(
        student_id INTEGER,
        percentage REAL
        )
        """)

        conn.commit()
        conn.close()

    # ------------------------
    # ADD STUDENT WINDOW
    # ------------------------

    def add_student_window(self):

        win = tk.Toplevel(self.root)
        win.title("Add Student")
        win.geometry("350x250")

        tk.Label(win, text="Student ID").pack(pady=5)
        sid = tk.Entry(win)
        sid.pack()

        tk.Label(win, text="Student Name").pack(pady=5)
        name = tk.Entry(win)
        name.pack()

        def save_student():

            s = sid.get()
            n = name.get()

            if s == "" or n == "":
                messagebox.showerror("Error", "Enter all fields")
                return

            conn = sqlite3.connect("college.db")
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "INSERT INTO students VALUES (?,?)",
                    (s, n)
                )
                conn.commit()
                messagebox.showinfo("Success", "Student Added")

                sid.delete(0, tk.END)
                name.delete(0, tk.END)

            except:
                messagebox.showerror("Error", "Student ID already exists")

            conn.close()

        tk.Button(win,
                  text="Add Student",
                  command=save_student).pack(pady=15)

    # ------------------------
    # VIEW STUDENT WINDOW
    # ------------------------

    def view_student_window(self):

        win = tk.Toplevel(self.root)
        win.title("View Students")
        win.geometry("500x350")

        table = ttk.Treeview(win,
                             columns=("id", "name"),
                             show="headings")

        table.heading("id", text="Student ID")
        table.heading("name", text="Student Name")

        table.pack(fill="both", expand=True)

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")

        rows = cursor.fetchall()

        for row in rows:
            table.insert("", tk.END, values=row)

        conn.close()

    # ------------------------
    # MERIT LIST WINDOW
    # ------------------------

    def merit_window(self):

        win = tk.Toplevel(self.root)
        win.title("Top 10 Merit List")
        win.geometry("500x350")

        table = ttk.Treeview(win,
                             columns=("id", "percentage"),
                             show="headings")

        table.heading("id", text="Student ID")
        table.heading("percentage", text="Percentage")

        table.pack(fill="both", expand=True)

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT student_id, percentage
        FROM results
        ORDER BY percentage DESC
        LIMIT 10
        """)

        rows = cursor.fetchall()

        for row in rows:
            table.insert("", tk.END, values=row)

        conn.close()


if __name__ == "__main__":

    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
