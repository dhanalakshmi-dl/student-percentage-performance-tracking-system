
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import matplotlib.pyplot as plt
import csv
from subjects import subjects

class StaffDashboard:

    def __init__(self,root):

        root.title("Staff Dashboard")
        root.geometry("600x500")

        tk.Label(root,text="ENTER MARKS",font=("Arial",18,"bold")).pack()

        tk.Label(root,text="Student ID").pack()
        self.sid=tk.Entry(root)
        self.sid.pack()

        tk.Label(root,text="Department").pack()
        self.dept=ttk.Combobox(root,values=list(subjects.keys()))
        self.dept.pack()

        tk.Label(root,text="Semester").pack()
        self.sem=tk.Entry(root)
        self.sem.pack()

        tk.Button(root,text="Load Subjects",command=self.load_subjects).pack()

        self.sub=ttk.Combobox(root)
        self.sub.pack()

        tk.Label(root,text="Internal (25)").pack()
        self.internal=tk.Entry(root)
        self.internal.pack()

        tk.Label(root,text="External (75)").pack()
        self.external=tk.Entry(root)
        self.external.pack()

        tk.Button(root,text="Save Marks",command=self.save).pack(pady=5)
        tk.Button(root,text="Graph",command=self.graph).pack()
        tk.Button(root,text="Export CSV",command=self.export).pack()

    def load_subjects(self):

        d=self.dept.get()
        s=int(self.sem.get())

        if d in subjects and s in subjects[d]:
            self.sub["values"]=subjects[d][s]

    def save(self):

        i=int(self.internal.get())
        e=int(self.external.get())

        total=i+e
        percentage=total

        conn=sqlite3.connect("college.db")
        cur=conn.cursor()

        cur.execute(
        "INSERT INTO marks(student_id,subject,internal,external,total,percentage) VALUES(?,?,?,?,?,?)",
        (self.sid.get(),self.sub.get(),i,e,total,percentage))

        conn.commit()
        conn.close()

        messagebox.showinfo("Saved","Marks saved")

    def graph(self):

        conn=sqlite3.connect("college.db")
        cur=conn.cursor()

        cur.execute("SELECT subject,total FROM marks WHERE student_id=?",(self.sid.get(),))
        rows=cur.fetchall()

        subjects=[r[0] for r in rows]
        marks=[r[1] for r in rows]

        plt.bar(subjects,marks)
        plt.title("Student Marks")
        plt.show()

    def export(self):

        conn=sqlite3.connect("college.db")
        cur=conn.cursor()

        cur.execute("SELECT * FROM marks WHERE student_id=?",(self.sid.get(),))
        rows=cur.fetchall()

        path=filedialog.asksaveasfilename(defaultextension=".csv")

        if path == "":
            return

        with open(path,"w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(["ID","Student","Subject","Internal","External","Total","Percentage"])
            writer.writerows(rows)

        conn.close()
