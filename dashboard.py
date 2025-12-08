from tkinter import *
from tkinter import messagebox
from db import get_connection
import login

def open_dashboard(employee_id, employee_name, login_root):

    window = Toplevel(login_root)
    window.title("Dashboard")
    window.geometry("400x300")

    Label(window, text=f"Welcome {employee_name}", font=("Arial", 14)).pack(pady=10)
    
    Button(window, text="Mark Attendance", command=lambda: mark_attendance(employee_id)).pack(pady=20)
    
    Button(window, text="Logout", command=lambda: logout(employee_id, window)).pack(pady=10)
    
    return window

def mark_attendance(employee_id):
    try:
        con = get_connection()
        cursor = con.cursor(buffered=True)
        cursor.execute("SELECT time_in FROM attendance WHERE employee_id=%s AND date=CURDATE()", (employee_id,))
        row = cursor.fetchone()
        if row:
            messagebox.showerror("Info", "You already logged in Today.")
            return
        
        cursor.execute("INSERT INTO attendance (employee_id, date, time_in) VALUES (%s, CURDATE(), CURTIME())", (employee_id,))
        con.commit()
    
        messagebox.showinfo("Success", "Attendance Marked!")
        
        cursor.close()
        con.close()

    except Exception as msg:
        messagebox.showerror("Error", str(msg))
        
        
def logout(employee_id, dashboard_window):
    try:
        con = get_connection()
        cursor = con.cursor(buffered=True)

        # Check today's attendance row
        cursor.execute("SELECT id, time_out FROM attendance WHERE employee_id=%s AND date=CURDATE()", (employee_id,))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Error", "You did not mark time in today.")
            return

        # If time_out already exists
        if row[1] is not None:
            messagebox.showinfo("Info", "You already marked out today.")
        else:
            # Update time_out with current time
            cursor.execute("UPDATE attendance SET time_out = CURTIME() WHERE id=%s", (row[0],))
            con.commit()
            messagebox.showinfo("Success", "Logged out successfully!")
            
        cursor.close()
        con.close()
        
        # Close dashboard
        dashboard_window.destroy()

        import login
        # Re-open the login window
        login.root.deiconify() # show login window again

    except Exception as msg:
        messagebox.showerror("Error", str(msg))