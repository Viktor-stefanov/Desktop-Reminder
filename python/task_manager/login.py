from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import validate_email
import string
import random
import time
from db import *
from PIL import ImageTk, Image
from date_time import get_countries
from send_mail import send_verification_email
from resource_path import resource_path


class LoginPage(Frame):
    location = None
    logged_in = False
    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.title("Login")
        x = int(self.root.winfo_screenwidth() / 4.5)
        y = int(self.root.winfo_screenheight() / 8)
        self.root.geometry(f"800x600+{x}+{y}")
        self.root.update()
        self.root.minsize(800, 600)
        self.root.maxsize(800, 600)
        self.width, self.height = self.root.winfo_width(), self.root.winfo_height()

        self.cwd = os.getcwd()
        self.login_page()
        self.root.mainloop()

    def login_page(self, clear=False):
        self.root.title("Login")
        # Try to delete the widgets from the other screen
        if clear is True:
            self.a = Label(self.root, text="Successful registration!", font="Verdana 14", fg="#E5F0D9").place(x=100, y=100)
            for widget in (self.second_pwd, self.second_pwd_entry, self.email_label, self.email_entry, self.have_account,
                           self.sign_in, self.register_btn, self.title, self.container, self.loc_label):
                widget.place_forget()

        self.pwd = StringVar()
        self.user_name = StringVar()
        title = Label(self.root, text="Task Manager", font="Verdana 36")
        self.title = Label(self.root, text="LOGIN", font="Verdana 24")
        un_label = ttk.Label(self.root, text="Username", font="Verdana 14")
        pwd_label = ttk.Label(self.root, text="Password", font="Verdana 14")
        self.un_entry = ttk.Entry(self.root, font="Verdana 14")
        self.pwd_entry = ttk.Entry(self.root, show="*", font="Verdana 14")
        self.photo = ImageTk.PhotoImage(Image.open(resource_path("password_eye.png")).resize((30, 20)))
        self.pwd_eye = Button(self.root, image=self.photo, borderwidth=0, command=lambda: self.eye())
        self.no_account = ttk.Label(self.root, text="Don't have an account?", font="verdana 10")
        self.login_btn = ttk.Button(self.root, text="Login", command=self.login, width=14)
        self.register_btn = ttk.Button(self.root, text="Register", command=self.register_page)

        title.place(x=self.width / 3.3, y=50)
        self.title.place(x=self.width / 2.3, y=150)
        un_label.place(x=self.width / 4, y=self.height / 2.3)
        self.un_entry.place(x=self.width / 2.5, y=self.height / 2.3)
        pwd_label.place(x=self.width / 4, y=self.height / 2)
        self.pwd_entry.place(x=self.width / 2.5, y=self.height / 2)
        self.pwd_eye.place(x=self.width / 1.4, y=self.height / 2)
        self.login_btn.place(x=self.width / 4, y=self.height / 1.7)
        self.no_account.place(x=self.width / 4, y=self.height / 1.55)
        self.register_btn.place(x=self.width / 2.15, y=self.height / 1.55)

    def register_page(self):
        # delete the widgets from the other screen
        for widget in (self.no_account, self.register_btn, self.login_btn):
            widget.place_forget()
        # add email and another password entry
        self.root.title("Register")
        self.title["text"] = "REGISTER"
        self.title.place(x=self.width / 2.5)
        self.second_pwd = ttk.Label(self.root, text="Confirm Password", font="Verdana 14")
        self.second_pwd_entry = ttk.Entry(self.root, font="Verdana 14", show=self.pwd_entry["show"])
        self.email_label = ttk.Label(self.root, text="E-mail", font="Verdana 14")
        self.email_entry = ttk.Entry(self.root, font="Verdana 14")
        self.loc_label = ttk.Label(self.root, text="Country", font="Verdana 14")
        countries = list(get_countries().keys())
        self.container = Frame(self.root, width=247, height=50)
        self.container.pack_propagate(False)
        self.combo = ttk.Combobox(self.container, value=countries, font="Verdana 14", state="readonly")
        self.combo.current(0)
        self.have_account = ttk.Label(self.root, text="Already have an account?", font="Verdana 10")
        self.sign_in = ttk.Button(self.root, text="Sign In", command=lambda: self.login_page(clear=True))
        self.register_btn = ttk.Button(self.root, text="Register", command=self.register)

        self.second_pwd.place(x=self.width / 6.8, y=self.height / 1.78)
        self.second_pwd_entry.place(x=self.width / 2.5, y=self.height / 1.78)
        self.email_label.place(x=self.width / 3.5, y=self.height / 1.6)
        self.email_entry.place(x=self.width / 2.5, y=self.height / 1.6)
        self.loc_label.place(x=self.width / 3.7, y=self.height / 1.45)
        self.container.place(x=self.width / 2.5, y=self.height / 1.45)
        self.combo.pack()
        self.have_account.place(x=self.width / 2.5, y=self.height / 1.28)
        self.sign_in.place(x=self.width / 1.6, y=self.height / 1.28, width=66)
        self.register_btn.place(x=self.width / 3.5, y=self.height / 1.28)

    def login(self):
        username = self.un_entry.get()
        pwd = self.pwd_entry.get()
        errors = []
        if len(username) == 0:
            errors.append("Please provide a user name")
        if len(pwd) == 0:
            errors.append("Please provide a password")

        if len(errors) > 0:
            messagebox.showwarning("Errors", "\n\n".join(errors))
        else:
            return_value = user_exists(username, pwd)
            if return_value != 1:
                messagebox.showwarning("Errors", "\n\n".join([return_value]))
            else:
                self.logged_in = True
                self.location = get_location(self.un_entry.get())[0]
                self.root.destroy()

    def register(self):
        valid_un_chars = string.ascii_letters + string.digits + "_-"
        self.username = self.un_entry.get()
        valid_pwd_chars = string.ascii_letters + string.digits
        self.pwd, pwd2 = self.pwd_entry.get(), self.second_pwd_entry.get()
        self.email = self.email_entry.get()

        errors = []
        # change un
        if len(self.username) == 0:
            errors.append("Please provide a username!")
        else:
            if any(ch not in valid_un_chars for ch in self.username):
                errors.append("Username can consist only of letters, numbers and a _!")
            if len(self.username) < 6:
                errors.append("Username should be at least 6 characters!")
        # change password
        if len(self.pwd) == 0:
            errors.append("Please provide a password!")
        else:
            if any(ch not in valid_pwd_chars for ch in self.pwd):
                errors.append("Password can consist only of letters and numbers!")
            if self.pwd != pwd2:
                errors.append("Confirmed password doesn't match the first one!")
            if len(self.pwd) < 6:
                errors.append("Password should be at least 6 characters!")
            if len(self.pwd) > 20:
                errors.append("Password can't be more than 20 characters!")
        # email isn't valid
        if len(self.email) == 0:
            errors.append("Please provide an e-mail!")
        elif any(symbol not in self.email for symbol in ("@", ".")):
            errors.append("Please provide a valid e-mail!")
        if validate_email.validate_email(self.email) is False:
            errors.append("The provided email doesn't exist!")

        if len(errors) > 0:
            messagebox.showwarning("Errors", "\n\n".join(errors))
        else:
            return_value = is_valid_name(self.username)
            if return_value != 1:
                messagebox.showwarning("Errors", "\n\n".join([return_value]))
            else:
                self.confirm_account()

    def confirm_account(self):
        receiver_email = self.email_entry.get()
        self.otp = generate_otp()
        self.start_time = time.time()

        messagebox.showinfo(message="Confirm your account with the code send to your email")
        self.window = Toplevel(self.root)
        self.window.title("Validate account")
        x = int(self.window.winfo_screenwidth() / 3.2)
        y = int(self.window.winfo_screenheight() / 4)
        self.window.geometry(f"290x90+{x}+{y}")

        self.otp_tries = 0
        Label(self.window, text="Enter OTP:", font="Helvetica 16").grid(row=0, column=0, pady=(15, 5), padx=(0, 5))
        Button(self.window, text="Confirm", font="Helvetica 12", command=self.otp_matches, width=10).grid(row=1, column=1, sticky=E, padx=(4))
        self.otp_entry = Entry(self.window, font="Helvetica 16", width=13)
        self.otp_entry.grid(row=0, column=1, padx=5, pady=(10, 0))

        return_value = send_verification_email(receiver_email, self.otp)
        if return_value != 1:
            print("THERE HAS BEEN AN ERROR VIKTOR FIX IT VIKTOR! :D")

    def otp_matches(self):
        user_otp = self.otp_entry.get()
        if user_otp != self.otp:  # user entered wrong OTP
            self.otp_tries += 1
            messagebox.showerror(message=f"Wrong OTP!", parent=self.window)
        else:  # user entered correct OTP
            location = self.combo.get()
            return_value = register_user(self.username, self.pwd, self.email, location)
            if return_value == 1:
                messagebox.showinfo("Info", "Successful registration!")
                self.window.destroy()
                self.login_page(clear=True)
            else:
                messagebox.showerror("Errors", "\n\n".join([return_value]))

        if self.otp_tries == 3 or (time.time() - self.start_time) / 60 > 10:
            self.window.destroy()

    def eye(self):
        if self.pwd_entry["show"] == "":
            self.pwd_entry["show"] = "*"
        else:
            self.pwd_entry["show"] = ""
        try:
            self.second_pwd_entry["show"] = self.pwd_entry["show"]
        except AttributeError:
            pass

def generate_otp():
    otp = []
    for i in range(6):
        otp.append(list(map(str, range(1, 10)))[int(random.random() * 8)])
    return "".join(otp)