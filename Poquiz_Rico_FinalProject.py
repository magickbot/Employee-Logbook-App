import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import pytz
import json
import os

PST = pytz.timezone('Asia/Manila')

class LogIOButton:
    def __init__(self, parent):
        self.parent = parent
        self.popup = tk.Toplevel(parent)
        self.popup.title("Log In / Log Out")
        self.popup.geometry("300x180+750+350")
        self.popup.config(background="#29728f")
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

        self.usernameLabel = tk.Label(self.popup, text="USERNAME", font='verdana 9 bold', bg="#29728f")
        self.usernameLabel.pack()
        self.username_entry = tk.Entry(self.popup)
        self.username_entry.pack()

        self.passwordLabel = tk.Label(self.popup, text="PASSWORD", font='verdana 9 bold', bg="#29728f")
        self.passwordLabel.pack()
        self.password_entry = tk.Entry(self.popup)
        self.password_entry.pack()
        
        self.confirm_button = tk.Button(self.popup, text="Submit", command=self.submit_user_entry)
        self.confirm_button.pack(pady=5)

        self.close_button = tk.Button(self.popup, text="Close", command=self.close_popup)
        self.close_button.pack()

    def close_popup(self):
        EmployeeLogbookApp.log_button.config(state=tk.NORMAL)
        self.popup.destroy()

    def submit_user_entry(self):
        EmployeeLogbookApp.log_button.config(state=tk.NORMAL)
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not os.path.exists("database.json"):
            with open("database.json", "w") as file:
                json.dump([], file)
        with open("database.json", "r") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
            
        found = False
        for user_data in existing_data:
            if user_data["username"] == username and user_data["password"] == password:
                found = True
                break
        
        if not found:
            messagebox.showerror("Error", "Invalid username or password.")
            return
        
        if not os.path.exists("logs.json"):
            with open("logs.json", "w") as file:
                json.dump([], file)
        with open("logs.json", "r") as file:
            try:
                logs_data = json.load(file)
            except json.JSONDecodeError:
                logs_data = []
        
        logged_in = False
        for log_data in logs_data:
            if log_data["username"] == username and log_data["logins"][-1]["logout_time"] is None:
                logged_in = True
                break
        
        current_time = datetime.now(PST)
        if logged_in:
            # User is logged in, record log out time
            for log_data in logs_data:
                if log_data["username"] == username and log_data["logins"][-1]["logout_time"] is None:
                    log_data["logins"][-1]["logout_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    break
        else:
            # User is not logged in, record log in time
            log_data = {
                "username": username,
                "logins": [
                    {
                        "login_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "logout_time": None
                    }
                ]
            }
            logs_data.append(log_data)

        
        # Write the updated logs data to the file
        with open("logs.json", "w") as file:
            json.dump(logs_data, file, indent=4)
        
        # Show a success messagebox
        if logged_in:
            messagebox.showinfo("Success", "Log Out successful.")
        else:
            messagebox.showinfo("Success", "Log In successful.")
        
        # Close the log in/out window
        self.close_popup()
 
class RegisterButton:
    def __init__(self, parent):
        self.parent = parent
        self.popup = tk.Toplevel(parent)
        self.popup.title("Registration Window")
        self.popup.geometry("300x300+750+350")
        self.popup.config(background="#29728f")
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)
        
        self.fullnameLabel = tk.Label(self.popup, text="FULL NAME", font='verdana 9 bold', bg="#29728f")
        self.fullnameLabel.pack()
        self.fullname_entry = tk.Entry(self.popup)
        self.fullname_entry.pack()

        self.usernameLabel = tk.Label(self.popup, text="USERNAME", font='verdana 9 bold', bg="#29728f")
        self.usernameLabel.pack()
        self.username_entry = tk.Entry(self.popup)
        self.username_entry.pack()

        self.passwordLabel = tk.Label(self.popup, text="PASSWORD", font='verdana 9 bold', bg="#29728f")
        self.passwordLabel.pack()
        self.password_entry = tk.Entry(self.popup)
        self.password_entry.pack()

        self.positionLabel = tk.Label(self.popup, text="POSITION", font='verdana 9 bold', bg="#29728f")
        self.positionLabel.pack()
        self.position_entry = tk.Entry(self.popup)
        self.position_entry.pack()
        
        self.departmentLabel = tk.Label(self.popup, text="DEPARTMENT", font='verdana 9 bold', bg="#29728f")
        self.departmentLabel.pack()
        self.department_entry = tk.Entry(self.popup)
        self.department_entry.pack()

        self.confirm_button = tk.Button(self.popup, text="Register", command=self.submit_user_entry)
        self.confirm_button.pack(pady=5)

        self.close_button = tk.Button(self.popup, text="Cancel", command=self.close_popup)
        self.close_button.pack(pady=5)
    
    def close_popup(self):
        EmployeeLogbookApp.reg_button.config(state=tk.NORMAL)
        self.popup.destroy()

    def submit_user_entry(self):
        EmployeeLogbookApp.reg_button.config(state=tk.NORMAL)
        fullname = self.fullname_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        position = self.position_entry.get()
        department = self.department_entry.get()

        if not os.path.exists("database.json"):
            with open("database.json", "w") as file:
                json.dump([], file)
        with open("database.json", "r") as file:
            try:
                existing_data = json.load(file)

                for user_data in existing_data:
                    if user_data["fullname"] == fullname:
                        messagebox.showerror("Error", "User already exists in the database.")
                        return
            except json.JSONDecodeError:
                existing_data = []

        user_data = {"fullname": fullname, "username": username, "password": password, "position": position, "department": department}

        if not existing_data:
            existing_data.append(user_data)
        else:
            usernames = [data.get("username") for data in existing_data]
            if username in usernames:
                messagebox.showerror("Error", "Username already exists in the database.")
                return

            existing_data.append(user_data)

        with open("database.json", "w") as file:
            json.dump(existing_data, file, indent=4)

        messagebox.showinfo("Success", "Registration successful.")
        self.popup.destroy()

class LogbookHistory:
    def __init__(self, parent):
        self.parent = parent
        self.popup = tk.Toplevel(parent)
        self.popup.title("Logbook History")
        self.popup.geometry("700x500+750+350")
        self.popup.config(background="white")
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)
        self.popup.resizable(False, False)

        self.frame1 = tk.Frame(self.popup, height=110, width=700, bg='#29728f', bd=1, relief=tk.FLAT)
        self.frame1.place(x=0, y=0)
        self.frame2 = tk.Frame(self.popup, height=30, width=700, bg='black', bd=1, relief=tk.FLAT)
        self.frame2.place(x=0, y=110)

        # Labels around the window
        self.history_table = tk.Label(self.popup, text="SEARCH RESULTS TABLE", font='verdana 9 bold', bg='black', fg='white')
        self.history_table.place(x=249, y=115)
        self.search_name_label = tk.Label(self.popup, text="Search username: ", font='verdana 9 bold', bg='#29728f', fg='black')
        self.search_name_label.place(x=20, y=20)
        self.search_date_label = tk.Label(self.popup, text="Search date: ", font='verdana 9 bold', bg='#29728f', fg='black')
        self.search_date_label.place(x=220, y=20)
        self.search_date_label2 = tk.Label(self.popup, text="YYYY-MM-DD", font='verdana 8 bold', bg='#29728f', fg='black')
        self.search_date_label2.place(x=220, y=60)

        # Treeview and its scrollbar
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", background="#a0c2c2")
        self.treev = ttk.Treeview(self.popup, selectmode ='browse', style="Custom.Treeview", height=16)
        self.treev.place(x=0, y=140)
        self.verscrlbar = ttk.Scrollbar(self.popup, orient ="vertical", command = self.treev.yview)
        self.verscrlbar.pack(side ='right', fill ='x')
        self.treev.configure(xscrollcommand = self.verscrlbar.set)

        # Treeview Contents
        self.treev["columns"] = ("Employee-Name", "Position", "Department", "Time in", "Time out")
        self.treev['show'] = 'headings'
        self.treev.column("Employee-Name", width = 139)
        self.treev.column("Position", width = 130)
        self.treev.column("Department", width = 130, anchor ='c')
        self.treev.column("Time in", width = 140, anchor ='c')
        self.treev.column("Time out", width = 140, anchor ='c')
        self.treev.heading("Employee-Name", text ="Employee-Name")
        self.treev.heading("Position", text ="Position")
        self.treev.heading("Department", text ="Department")
        self.treev.heading("Time in", text ="Time in")
        self.treev.heading("Time out", text ="Time out")
        
        # Auto insert current date logs to table
        current_time = datetime.now(PST)
        current_date = current_time.strftime("%Y-%m-%d")
        with open("database.json", "r") as d:
            with open("logs.json", "r") as l:
                self.json_db = json.load(d)
                json_log = json.load(l)
        for self.employee in json_log:
            try:
                if self.employee["logins"][0]["login_time"][:10] == current_date:
                    self.load_table()
                elif self.employee["logins"][0]["logout_time"][:10] == current_date:
                    self.load_table()
            except TypeError:
                if self.employee["logins"][0]["login_time"][:10] == current_date:
                    self.load_table()

        # Search options
        self.search_date_var = tk.StringVar()
        self.search_date = tk.Entry(self.popup, width = 12, bg = 'white', fg= 'black', textvariable = self.search_date_var, font='verdana 8')
        self.search_date['textvariable'] = self.search_date_var
        self.search_date.place(x= 220, y=40)

        self.search_name_var = tk.StringVar()
        self.search_name = tk.Entry(self.popup, width = 27, bg = 'white', fg= 'black', textvariable = self.search_name_var, font='verdana 8')
        self.search_name['textvariable'] = self.search_name_var
        self.search_name.place(x= 20, y=40)

        self.search_button = tk.Button(self.popup, text="Search", font='verdana 8 bold', width=6, height=1, relief=tk.RAISED, command=self.search_function)
        self.search_button.place(x= 313, y=37)

    def clear_result_box(self):
        self.treev.delete(*self.treev.get_children())
        
    def search_function(self): 
        self.clear_result_box()
        searched_d = self.search_date_var.get().strip()
        searched_n = self.search_name_var.get().strip()
        if searched_n == "" and searched_d == "":
                messagebox.showerror("Error", "Search entries are empty")
        with open("database.json", "r") as d:
            with open("logs.json", "r") as l:
                self.json_log = json.load(l)
                self.json_db = json.load(d)
        for self.employee in self.json_log:
            try: 
                if searched_n == self.employee["username"]:
                    if searched_d == self.employee["logins"][0]["login_time"][:10]:
                        self.load_table()
                        if searched_d == self.employee["logins"][0]["logout_time"][:10]:
                            self.load_table()
                    elif searched_d == self.employee["logins"][0]["logout_time"][:10]:
                        self.load_table()
                    elif searched_d == "":
                        self.load_table()
                elif searched_d == self.employee["logins"][0]["login_time"][:10] and searched_n == "":        
                    if searched_d == self.employee["logins"][0]["logout_time"][:10]:
                        self.load_table()
                    else:
                        self.load_table()
                elif searched_d == self.employee["logins"][0]["logout_time"][:10] and searched_n == "":
                        self.load_table()
            except TypeError:
                if searched_n == self.employee["username"]:
                    if searched_d == "":
                        self.load_table()
                elif searched_n == "" and searched_d == self.employee["logins"][0]["login_time"][:10]:
                    self.load_table()


    def load_table(self):
        log_in = self.employee["logins"][0]["login_time"]
        log_out = self.employee["logins"][0]["logout_time"]
        for db_employee in self.json_db:
            if self.employee["username"] == db_employee["username"]:
                emp_name = db_employee["fullname"]
                position = db_employee["position"]
                department = db_employee["department"]
                    
                self.treev.insert("", 'end', text ="L1", values =(emp_name, position, department, log_in, log_out))

    def close_popup(self):
        EmployeeLogbookApp.history_button.config(state=tk.NORMAL)
        self.popup.destroy()

class EmployeeLogbookApp:
    def __init__(self):
        self.app = tk.Tk()
        self.current_time = None
        self.current_date = None
        self.log_button = tk.Button(self.app, text="LOG IN / LOG OUT", command=self.loginlogout)
        self.log_button.pack(pady=50)

        self.setup_main_window()

    def setup_main_window(self):
        self.app.geometry("800x500+600+250")
        self.app.title("Employee Logbook System")
        self.app.resizable(False, False)
        self.app.config(background="#a0c2c2")
        
        frame1 = tk.Frame(self.app, height=110, width=800, bg='#29728f', bd=1, relief=tk.FLAT)
        frame1.place(x=0, y=0)
        frame2 = tk.Frame(self.app, height=30, width=800, bg='black', bd=1, relief=tk.FLAT)
        frame2.place(x=0, y=110)

        self.current_time = tk.Label(self.app, text="Current Time", font='timesnewroman 18 bold', bg="#29728f")
        self.current_time.place(x=275, y=5)

        self.current_date = tk.Label(self.app, text="Current Date", font='timesnewroman 12 bold', bg="#29728f")
        self.current_date.place(x=300, y=40)

        EmployeeLogbookApp.log_button = tk.Button(self.app, text='LOG IN / LOG OUT', font='verdana 9 bold', width=17, height=1, relief=tk.RAISED, command=self.loginlogout)
        EmployeeLogbookApp.log_button.place(x=90, y=70)

        EmployeeLogbookApp.reg_button = tk.Button(self.app, text='REGISTER', font='verdana 9 bold', width=9, height=1, relief=tk.RAISED, command=self.register)
        EmployeeLogbookApp.reg_button.place(x=305, y=75)

        EmployeeLogbookApp.history_button = tk.Button(self.app, text='LOGBOOK HISTORY', font='verdana 9 bold', width=17, height=1, relief=tk.RAISED, command=self.call_table)
        EmployeeLogbookApp.history_button.place(x=460, y=70)

        self.search_button = tk.Button(self.app, text="REFRESH", font='verdana 9 bold', width=9, height=1, relief=tk.RAISED, command=self.see_todays)
        self.search_button.place(x= 10, y=112)

        self.today_table = tk.Label(self.app, text="TODAY'S LOG", font='verdana 9 bold', bg='black', fg='white')
        self.today_table.place(x=300, y=115)

        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", background="#a0c2c2")

        self.treev = ttk.Treeview(self.app, selectmode ='browse', style="Custom.Treeview", height=16)
        self.treev.place(x=0, y=140)
        
        self.verscrlbar = ttk.Scrollbar(self.app, orient ="vertical", command = self.treev.yview)
        self.verscrlbar.pack(side ='right', fill ='x')

        self.treev.configure(xscrollcommand = self.verscrlbar.set)
        self.treev["columns"] = ("Status", "Employee-Name", "Position", "Department", "Time in", "Time out")
        self.treev['show'] = 'headings'
        
        self.treev.column("Status", width = 120, anchor ='c')
        self.treev.column("Employee-Name", width = 130)
        self.treev.column("Position", width = 120)
        self.treev.column("Department", width = 120, anchor ='c')
        self.treev.column("Time in", width = 145, anchor ='c')
        self.treev.column("Time out", width = 145, anchor ='c')
        
        self.treev.heading("Status", text ="Status")
        self.treev.heading("Employee-Name", text ="Employee-Name")
        self.treev.heading("Position", text ="Position")
        self.treev.heading("Department", text ="Department")
        self.treev.heading("Time in", text ="Time in")
        self.treev.heading("Time out", text ="Time out")
        
        self.see_todays()


    def see_todays(self):
        self.clear_result_box()
        current_time_4logtable = datetime.now(PST)
        current_date_4logtable = current_time_4logtable.strftime("%Y-%m-%d")
        with open("database.json", "r") as d:
            with open("logs.json", "r") as l:
                json_db = json.load(d)
                json_log = json.load(l)
        for newly_registered in json_db:
            status = "Not Working Yet"
            log_in = "--:--:--"
            log_out = "--:--:--"
            emp_name = newly_registered["fullname"]
            position = newly_registered["position"]
            department = newly_registered["department"]
            for employee in json_log:
                if newly_registered["username"] == employee["username"] and employee["logins"][0]["login_time"][:10] == current_date_4logtable:
                    log_in = employee["logins"][0]["login_time"]
                    log_out = employee["logins"][0]["logout_time"]
                    if log_out is None:
                        status = "Working"
                        log_out = "--:--:--"
                    elif log_out is not None:
                        status = "Already left"
                try:
                    if newly_registered["username"] == employee["username"] and employee["logins"][0]["logout_time"][:10] == current_date_4logtable:
                        log_in = employee["logins"][0]["login_time"]
                        log_out = employee["logins"][0]["logout_time"]
                        status = "Already left"
                except TypeError:
                    pass

            self.treev.insert("", 'end', text ="L1", values =(status, emp_name, position, department, log_in, log_out))

    def clear_result_box(self):
        self.treev.delete(*self.treev.get_children())

    def call_table(self):
        EmployeeLogbookApp.history_button.config(state=tk.DISABLED)
        LogbookHistory(self.app)

    def loginlogout(self):
        EmployeeLogbookApp.log_button.config(state=tk.DISABLED)
        LogIOButton(self.app)

    def register(self):
        EmployeeLogbookApp.reg_button.config(state=tk.DISABLED)
        RegisterButton(self.app)
    
    def update_clock(self):
        raw_TS = datetime.now(PST)
        date_now = raw_TS.strftime("%d %b %Y")
        time_now = raw_TS.strftime("%H:%M:%S %p")
        self.current_time.config(text=time_now)
        self.current_date.config(text=date_now)
        self.current_time.after(1000, self.update_clock)

    def run(self):
        self.update_clock()
        self.app.mainloop()


# Create an instance of the EmployeeLogbookApp class and run the application
if __name__ == '__main__':
    app = EmployeeLogbookApp()
    app.run()
