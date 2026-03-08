
import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt

class StudentDashboard:

    def __init__(self,root):

        root.title("Student Result")
        root.geometry("600x500")

        tk.Label(root,text="Student Result",font=("Arial",20)).pack()

        tk.Label(root,text="Student ID").pack()
        self.sid=tk.Entry(root)
        self.sid.pack()

        tk.Button(root,text="Show Result",command=self.show).pack()

        self.table = ttk.Treeview(root,columns=("subject","internal","external","total","percentage"),
show="headings")

        self.table.heading("subject", text="Subject")
        self.table.heading("internal", text="Internal")
        self.table.heading("external", text="External")
        self.table.heading("total", text="Total")
        self.table.heading("percentage", text="Percentage")

        self.table.pack(fill="both", expand=True)

        tk.Button(root,text="Graph",command=self.graph).pack()

    def show(self):

        conn=sqlite3.connect("college.db")
        cur=conn.cursor()

        cur.execute(
"SELECT subject,internal,external,total,percentage FROM marks WHERE student_id=?",
(self.sid.get(),)
)
        
        for r in cur.fetchall():
            self.table.insert("",tk.END,values=r)

        conn.close()

    def graph(self):

        conn=sqlite3.connect("college.db")
        cur=conn.cursor()

        cur.execute("SELECT subject,total FROM marks WHERE student_id=?",(self.sid.get(),))
        rows=cur.fetchall()

        subjects=[r[0] for r in rows]
        marks=[r[1] for r in rows]

        plt.bar(subjects,marks)
        plt.title("Result Graph")
        plt.show()
