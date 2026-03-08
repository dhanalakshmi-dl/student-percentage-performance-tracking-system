
import tkinter as tk
from database import create_database
from login import LoginPage

create_database()

root = tk.Tk()
root.title("College Performance System")
root.geometry("800x500")

LoginPage(root)

root.mainloop()
