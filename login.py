import tkinter as tk
from tkinter import *
from tkinter import messagebox
from db import get_connection

root = None
username_entry = None
pass_entry = None

def open_login_window():
    global root, username_entry, pass_entry
    
    root = Tk(className="login")
    root.geometry("400x300")
    l = Label(root, text='Employee Attendance System')
    l.grid(row = 1, column= 1, pady= 10)
    
    user_name = Label(root, text='Username')
    user_pass = Label(root, text='Password')
    user_name.grid(row=2, column=0)
    user_pass.grid(row=3, column=0)

    username_entry = Entry(root)
    pass_entry = Entry(root, show="*")
    username_entry.grid(row=2, column=1)
    pass_entry.grid(row=3, column=1)
    
    button = Button(root, text='Submit', width=20, command=login_user)
    button.grid(padx=10, pady=10, row=4, column=1)

    root.mainloop()

def login_user():
    global root
    u_name = username_entry.get()
    u_pwd = pass_entry.get()

    con = get_connection()
    if con is None:
        messagebox.showerror("Error", "Database connection failed")
    cursor = con.cursor(buffered=True)
    cursor.execute("SELECT id, name, password FROM employees WHERE username = %s", (u_name,))
    
    row = cursor.fetchone()
    if not row:
        messagebox.showerror("Error", "Invalid-Username or Password")
        return

    
    employee_id = row[0]
    employee_name = row[1]
    password_ = row[2]

    if password_ == u_pwd:
        messagebox.showinfo("Success", "Login Successful")
        
        clear_inputs()
        cursor.close()
        con.close()
        
        root.withdraw()   # hides login, does NOT destroy it
        
        from dashboard import open_dashboard
        open_dashboard(employee_id, employee_name, root)
        
    else:
        messagebox.showerror("Error", "Invalid Username or Password")
        cursor.close()
        con.close()
        
def clear_inputs():
    username_entry.delete(0, END)
    pass_entry.delete(0, END)