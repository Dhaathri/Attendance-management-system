import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

FILE_NAME = "attendance.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Student", "Date", "Status"])
    df.to_csv(FILE_NAME, index=False)


def mark_attendance():
    name = name_entry.get().strip()
    date = date_entry.get().strip()
    status = status_var.get()

    if not name or not date:
        messagebox.showerror("ERROR", "Please fill all fields!")
        return

    new_record = pd.DataFrame({
        "Student": [name],
        "Date": [date],
        "Status": [status]
    })

    df = pd.read_csv(FILE_NAME)#existing csv to df
    df = pd.concat([df, new_record], ignore_index=True)#adding new records without indexes
    df.to_csv(FILE_NAME, index=False)#df to csv

    messagebox.showinfo("Success", "Attendance Marked Successfully!")
#resetting the inputs for next record
    name_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


def view_attendance():
    df = pd.read_csv(FILE_NAME)

    #new  window for attendance records
    view_window = tk.Toplevel(root)
    view_window.title("Attendance Records")
    view_window.geometry("500x300")
    
    #displaying data in table format in view_window
    tree = ttk.Treeview(
        view_window,
        columns=("Student", "Date", "Status"),
        show="headings"
    )

    tree.heading("Student", text="Student")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")

    tree.pack(fill="both", expand=True)

    for i in df.values.tolist():
        tree.insert("", tk.END, values=i)



# Main Window
root = tk.Tk()
root.title("Attendance Management System")
root.geometry("400x300")

title = tk.Label(
    root,
    text="Attendance Management System",
    font=("Arial", 14, "bold")
)
title.pack(pady=10)

# Student Name
tk.Label(root, text="Student Name").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# Date
tk.Label(root, text="Date (DD-MM-YYYY)").pack()
date_entry = tk.Entry(root, width=30)
date_entry.pack(pady=5)

# Attendance Status
tk.Label(root, text="Status").pack()
status_var = tk.StringVar(value="P")

ttk.Radiobutton(root, text="Present", variable=status_var, value="P").pack()
ttk.Radiobutton(root, text="Absent", variable=status_var, value="A").pack()

# Buttons
tk.Button(root,text="Mark Attendance",command=mark_attendance,bg="lightgreen").pack(pady=10)
tk.Button(root,text="View Attendance",command=view_attendance,bg="lightblue").pack()

root.mainloop()
