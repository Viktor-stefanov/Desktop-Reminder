from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from db import *
from date_time import get_countries


class Options:
    location = None

    def __init__(self, master):
        if len(master.winfo_children()) == 0:
            Label(master, text="Account Options", font="Helvetica 48", bg="#dbd9d9").pack(pady=(0, 110))
            change_un = Button(master, text="Change Username", font="Helvetica 20", command=lambda: self.change_username_window(master), bg="#dbd9d9", borderwidth=0)
            change_pwd = Button(master, text="Change Password", font="Helvetica 20", command=lambda: self.change_pwd_window(master), bg="#dbd9d9", borderwidth=0)
            change_email = Button(master, text="Change E-mail", font="Helvetica 20", command=lambda: self.change_email_window(master), bg="#dbd9d9", borderwidth=0)
            set_location = Button(master, text="Change Country", font="Helvetica 20", command=lambda: self.set_location_window(master), bg="#dbd9d9", borderwidth=0)

            change_un.pack(pady=5)
            change_pwd.pack()
            change_email.pack(pady=5)
            set_location.pack()

    def show_window(self, master):
        self.window = Toplevel(master)
        x = self.window.winfo_screenwidth() // 3
        y = self.window.winfo_screenheight() // 6
        self.window.title("Change username")
        self.window.geometry(f"500x275+{x}+{y}")

        type_un = Label(self.window, text="Enter current username:", font="Helvetica 16")
        self.type_un_entry = Entry(self.window, font="Helvetica 16", width=18)
        type_pwd = Label(self.window, text="Enter password:", font="Helvetica 16")
        self.type_pwd_entry = Entry(self.window, font="Helvetica 16", width=18, show="*")
        self.photo = ImageTk.PhotoImage(Image.open(r"C:\Users\leagu\PycharmProjects\taskManager\img\password_eye.png").resize((30, 20)))
        pwd_eye = Button(self.window, image=self.photo, borderwidth=0, command=lambda: self.eye())

        type_un.grid(row=1, column=0, sticky=E, padx=10)
        self.type_un_entry.grid(row=1, column=1)
        type_pwd.grid(row=2, column=0, sticky=E, padx=10, pady=5)
        self.type_pwd_entry.grid(row=2, column=1)
        pwd_eye.grid(row=2, column=2)

    def change_username_window(self, master):
        self.show_window(master)
        Label(self.window, text="Change Username", font="Verdana 24").grid(row=0, column=0, columnspan=3, sticky="NESW", pady=(40, 25))
        self.submit_btn = Button(self.window, text="Submit", width=10, font="Helvetica 12", borderwidth=1, command=lambda: self.validate_credentials("un"))
        self.submit_btn.grid(row=3, column=1, sticky=E, pady=5)

    def change_pwd_window(self, master):
        self.show_window(master)
        Label(self.window, text="Change Password", font="Verdana 24").grid(row=0, column=0, columnspan=3, sticky="NSEW", pady=(40, 25))
        self.submit_btn = Button(self.window, text='Submit', width=10, font="Helvetica 12", borderwidth=1, command=lambda: self.validate_credentials("pwd"))
        self.submit_btn.grid(row=3, column=1, sticky=E, pady=5)

    def change_email_window(self, master):
        self.show_window(master)
        Label(self.window, text="Change Email", font="Verdana 24").grid(row=0, column=0, columnspan=3, sticky="NSEW", pady=(40, 25))
        self.submit_btn = Button(self.window, text='Submit', width=10, font="Helvetica 12", borderwidth=1, command=lambda: self.validate_credentials("email"))
        self.submit_btn.grid(row=3, column=1, sticky=E, pady=5)

    def set_location_window(self, master):
        self.show_window(master)
        self.window.title("Set Location")
        x = self.window.winfo_screenwidth() // 3
        y = self.window.winfo_screenheight() // 10
        self.window.geometry(f"505x290+{x}+{y}")

        Label(self.window, text="Change Country", font="Verdana 24").grid(row=0, column=0, columnspan=3, sticky="NSEW", pady=(40, 25))

        countries = list(get_countries().keys())
        combo = ttk.Combobox(self.window, value=countries, font="Helvetica 16", state="readonly")
        combo.current(0)
        combo.grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=(15, 0), pady=(10, 0))

        style = ttk.Style()

        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

        Button(self.window, text="Submit country", font="Helvetica 14", borderwidth=1, command=lambda: self.set_location(combo.get())).grid(row=4, column=1, sticky=E)

    def validate_credentials(self, task):
        name = self.type_un_entry.get()
        pwd = self.type_pwd_entry.get()
        return_value = user_exists(name, pwd)
        if return_value == 1:
            self.submit_btn.destroy()
            if task == "un":
                new_un = Label(self.window, text="Enter new username:", font="Helvetica 16")
                self.new_un_entry = Entry(self.window, font="Helvetica 16", width=18)
                change_un = Button(self.window, text="Change username", font="Helvetica 12", command=self.change_username)
                new_un.grid(row=3, column=0, padx=10)
                self.new_un_entry.grid(row=3, column=1)
                change_un.grid(row=4, column=1, sticky=E, pady=5)
            elif task == "pwd":
                new_pwd = Label(self.window, text="Enter new password:", font="Helvetica 16")
                self.new_pd_entry = Entry(self.window, font="Helvetica 16", width=18, show="*")
                change_pwd = Button(self.window, text="Change password", font="Helvetica 12", command=self.change_pwd)
                new_pwd.grid(row=3, column=0, padx=10)
                self.new_pd_entry.grid(row=3, column=1)
                change_pwd.grid(row=4, column=1, sticky=E, pady=5)
            elif task == "email":
                new_email = Label(self.window, text="Enter new e-mail", font="Helvetica 16")
                self.new_email_entry = Entry(self.window, font="helvetica 16", width=18)
                change_email = Button(self.window, font="Helvetica 12", command=self.change_email)
                new_email.grid(row=3, column=0, padx=10)
                self.new_email_entry.grid(row=3, column=1)
                change_email.grid(row=4, column=1, sticky=E, pady=5)
        else:
            messagebox.showwarning("Errors", "\n\n".join([return_value]), parent=self.window)

    def change_pwd(self):
        un = self.type_un_entry.get()
        pwd = self.type_pwd_entry.get()
        new_pwd = self.new_pd_entry.get()
        return_value = edit_password(un, pwd, new_pwd)
        if return_value == 1:
            self.window.destroy()
            messagebox.showinfo(message="Successful password change")
        else:
            messagebox.showerror("Errors", "\n\n".join([return_value]), parent=self.window)

    def change_username(self):
        old = self.type_un_entry.get()
        new = self.new_un_entry.get()
        return_value = edit_username(old, new)
        if return_value == 1:
            self.window.destroy()
            messagebox.showinfo(message="Successful username change")
        else:
            messagebox.showerror("Errors", "\n\n".join([return_value]), parent=self.window)

    def change_email(self):
        new = self.new_email_entry.get()
        return_value = is_valid_email(new)
        if return_value == 1:
            self.window.destroy()
            messagebox.showinfo(message="Successful e-mail change")
        else:
            messagebox.showerror(message="".join([return_value]), parent=self.window)

    def set_location(self, chosen):
        username = self.type_un_entry.get()
        password = self.type_pwd_entry.get()
        return_value = user_exists(username, password)
        if return_value == 1:
            edit_location(username, chosen)
            self.window.destroy()
        else:
            messagebox.showerror(message="".join([return_value]), parent=self.window)

    def eye(self):
        if self.type_pwd_entry["show"] == "":
            self.type_pwd_entry["show"] = "*"
        else:
            self.type_pwd_entry["show"] = ""