import re
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from login import LoginPage
from options import Options
from tracker import Tracker
from date_time import weekday_to_time
from resource_path import resource_path


class TaskManager(Frame):
    location = None
    completed_tasks = [0] * 7
    def __init__(self):
        l = LoginPage()
        self.location = l.location
        if l.logged_in is True:
            self.main_screen()
        self.main_screen()

    def main_screen(self):
        # colors = #B1A296 #557A95 #7395AE #379683 #5D5C61
        self.root = Tk()
        self.root.bind("<Button-1>", lambda e: self.root.update())
        self.root.configure(background="#dbd9d9")
        x = self.root.winfo_screenwidth() // 9
        y = self.root.winfo_screenheight() // 30
        self.root.geometry(f"1200x900+{x}+{y}")
        self.root.minsize(1200, 900)
        self.root.maxsize(1200, 900)
        self.root.columnconfigure(1, weight=2)

        self.tasks_img = ImageTk.PhotoImage(Image.open(resource_path("tasks.png")).resize((80, 300)))
        self.tracker_img = ImageTk.PhotoImage(Image.open(resource_path("tracker.png")).resize((80, 300)))
        self.options_img = ImageTk.PhotoImage(Image.open(resource_path("options.png")).resize((80, 300)))
        self.add_task_img = ImageTk.PhotoImage(Image.open(resource_path("add_task.png")).resize((30, 30)))
        self.delete_task_img = ImageTk.PhotoImage(Image.open(resource_path("delete.jpg")).resize((25, 25)))
        self.update_task_img = ImageTk.PhotoImage(Image.open(resource_path("edit.jpg")).resize((25, 25)))
        self.on_image = ImageTk.PhotoImage(Image.open(resource_path("unchecked.png")).resize((25, 25)))
        self.off_image = ImageTk.PhotoImage(Image.open(resource_path("checked.png")).resize((25, 25)))

        self.tasks_frame = Frame(self.root)
        self.tasks_btn = Button(self.root, image=self.tasks_img, borderwidth=0, command=self.tasks)
        self.tasks_btn.grid(row=0, column=0, sticky=W)
        self.tracker_frame = Frame(self.root)
        self.tracker_btn = Button(self.root, image=self.tracker_img, borderwidth=0, command=self.tracker)
        self.tracker_btn.grid(row=1, column=0, sticky=W)
        self.options_frame = Frame(self.root)
        self.options_btn = Button(self.root, image=self.options_img, borderwidth=0, command=self.options)
        self.options_btn.grid(row=2, column=0, sticky=W)
        self.current_frame = self.tasks_frame
        self.style = ttk.Style()
        self.style.theme_create("MyStyle", parent="alt", settings={
            "TNotebook.Tab": {"configure": {"padding": [48, 20], "background": "#B1A296", "foreground": "#edeff0",
                                            "font": "Helvetica 12"}}})
        self.tasks()
        self.root.mainloop()

    def options(self):
        self.current_frame.grid_forget()
        self.current_frame = self.options_frame
        self.options_frame.grid(row=0, column=1, rowspan=3, sticky=EW, pady=(0, 250))
        self.options_frame.configure(background="#dbd9d9")
        self.options = Options(self.options_frame)

    def tracker(self):
        self.current_frame.grid_forget()
        self.current_frame = self.tracker_frame
        self.tasks_frame.grid_forget()
        self.tracker_frame.grid(row=0, column=1, rowspan=3, sticky=NSEW)
        self.tracker_frame.configure(background="#dbd9d9")

        # calculate the amount of tasks each day has by first getting a number of children the day has, and then if the last label isn't empty increment this number by one (fixes the bug where it will still display 0 tasks when there is 1 task)
        weekday_tasks = [0] * 7
        for idx, weekday in enumerate((self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday)):
            # get all the tasks there are
            last_label = [child for child in weekday.winfo_children() if "label" in child.winfo_name()][-1]
            tasks = len(weekday.winfo_children()) - 4
            if tasks >= 0 and last_label["text"] != " ":
                tasks += 1
            weekday_tasks[idx] = tasks

        self.tracker = Tracker(self.tracker_frame, weekday_tasks, self.completed_tasks)

    def tasks(self):
        self.current_frame.grid_forget()
        self.current_frame = self.tasks_frame
        self.tasks_frame.grid(row=0, column=1, rowspan=3, sticky=NW)
        if len(self.tasks_frame.winfo_children()) == 0:
            self.style.theme_use("MyStyle")
            self.tasks_nb = ttk.Notebook(self.tasks_frame)
            self.tasks_nb.pack()

            self.monday = self.create_day_frame("Monday")
            self.tuesday = self.create_day_frame("Tuesday")
            self.wednesday = self.create_day_frame("Wednesday")
            self.thursday = self.create_day_frame("Thursday")
            self.friday = self.create_day_frame("Friday")
            self.saturday = self.create_day_frame("Saturday")
            self.sunday = self.create_day_frame("Sunday")

            for frame, name in ((self.monday, "Monday"), (self.tuesday, "Tuesday"), (self.wednesday, "Wednesday"),
                                (self.thursday, "Thursday"), (self.friday, "Friday"), (self.saturday, "Saturday"),
                                (self.sunday, "Sunday")):
                self.tasks_nb.add(frame, text=name)
            self.add_location()

    def add_location(self):
        for i, child in enumerate(self.tasks_nb.winfo_children()):
            date = weekday_to_time(self.location, i)
            date_label = Button(child, text=date, font="Helvetica 18", bg="#dbd9d9", borderwidth=0)
            date_label.place(x=25, y=200)

    def create_empty_label(self, day, ftb=False):
        text = Label(day, text=" ", font="Verdana 24", anchor=W)
        text.pack_propagate(False)
        delete_task_btn = Button(text, image=self.delete_task_img, borderwidth=0, bg="#dbd9d9",
                                 command=lambda: self.delete_task(text))
        update_task_btn = Button(text, image=self.update_task_img, borderwidth=0, bg="#dbd9d9",
                                 command=lambda: self.edit_task_window(text))

        delete_task_btn.pack(side=RIGHT)
        update_task_btn.pack(side=RIGHT, padx=5)

        if ftb is True:
            v = IntVar()
            finish_task_btn = Checkbutton(text, image=self.on_image, selectimage=self.off_image, indicatoron=False,
                                          onvalue=1, offvalue=0, variable=v, borderwidth=0, command=lambda: self.complete_task(day, v))
            finish_task_btn.pack(side=RIGHT)

        return text

    def complete_task(self, day, v):
        day = day.winfo_name()[-1]
        if day == "e":
            day = 1
        day = int(day) - 1

        if v.get() == 1:
            self.completed_tasks[day] += 1
        else:
            self.completed_tasks[day] -= 1

    def create_day_frame(self, name):
        day = Frame(self.tasks_nb, height=845, bg="#dbd9d9")
        day.pack(fill=BOTH, expand=True)
        day.pack_propagate(False)

        tasks = Label(day, text=f"{name}'s tasks: ", font="Helvetica 36", bg="#dbd9d9")
        tasks.pack(pady=75)

        # add the add task, delete, update buttons
        self.text = self.create_empty_label(day)
        self.add_task_btn = Button(day, image=self.add_task_img, borderwidth=0, bg="#dbd9d9",
                                   command=lambda: self.add_task_window(day))
        self.add_task_btn.pack(side=TOP, anchor=NE, padx=25)
        self.text.pack(padx=25, pady=(5, 0), fill=BOTH)

        return day

    def get_task_number(self, master):
        task_num = len(master.winfo_children()) - 4
        last_label = [child for child in master.winfo_children() if "label" in child.winfo_name()][-1]
        if task_num >= 1 and last_label["text"] != " ":
            task_num += 1

        return task_num

    def add_task_window(self, master):
        # add a task to the tasks Text widget
        self.window = Toplevel(master)
        self.window.focus_set()
        x = int(master.winfo_width() / 2.1)
        y = int(master.winfo_height() / 3)
        self.window.geometry(f"600x250+{x}+{y}")
        self.window.focus_set()
        self.root.bind("<FocusIn>", lambda e: self.window.destroy())
        self.window.title("Add Task")
        self.window.pack_propagate(False)

        task_number = self.get_task_number(master)
        label = Label(self.window, text=f"Add Task #{task_number}", font="Helvetica 24")
        label.pack(fill=BOTH, pady=(30, 0))
        # have something like 'add task #x' etc..
        self.task_text = Text(self.window, font="Verdana 14", height=3)
        self.task_text.pack(fill=BOTH, pady=(30, 0))
        # optional set time
        set_time = Label(self.window, text="Set time (optional) - ", font="Helvetica 16")
        set_time.pack(side=LEFT)

        self.hour_variable = StringVar()
        self.set_hour = Entry(self.window, font="Helvetica 18", width=5, textvariable=self.hour_variable)
        self.set_hour.pack(side=LEFT)
        reg = self.root.register(self.hour_checker)
        self.set_hour.config(validate="key", validatecommand=(reg, "%S", "%P", "%d"))

        add_task_btn = Button(self.window, text="Add Task", command=lambda: self.add_task(master, task_number),
                              font="Helvetica 12")
        add_task_btn.pack(side=RIGHT, padx=20)

    def hour_checker(self, key, string, a):
        # messy validation function
        if len(string) > 5:
            return False
        if a == "0":  # if the action is deleting
            return True
        if key.isnumeric():
            if len(string) == 1:
                if int(key) > 2:
                    return False
            elif len(string) == 2:
                if int(string) > 23:
                    return False
            elif len(string) == 4:
                if int(key) > 5:
                    return False
            elif len(string) == 5:
                if int(key) > 9:
                    return False
            elif len(string) == 3:
                return False
            return True
        elif any(ch in key for ch in (",", ".", ":")) and len(string) == 3:
            return True
        return False

    def add_task(self, master, task_num):
        label = master.nametowidget(
            sorted(list(child.winfo_name() for child in master.winfo_children()))[-2])  # DON"T EVER LOOK AT THIS
        task = self.task_text.get("1.0", "end-1c")
        # fetch the time if there is any
        if (time := self.set_hour.get()) != "":
            if all([ch.isnumeric() or ch in (":", ",", ".") for ch in time]):
                if len(time) == 3:
                    time = time[:2]
                elif len(time) == 4:
                    time = time[:3] + "0" + time[-1]
                task = task + " at " + time

        txt = self.create_empty_label(master, ftb=True)
        txt["text"] = f"#{str(task_num)}. {task}"
        if task_num == 1:
            label.destroy()
            txt.pack(padx=25, pady=(5, 0), fill=BOTH)
        else:
            txt.pack(padx=25, fill=BOTH)

        self.window.destroy()

    def edit_task_window(self, master):
        self.window = Toplevel(master)
        x = int(master.winfo_width() / 2.1)
        y = int(master.winfo_height() / 3)
        self.window.geometry(f"600x250+{x}+{y}")
        self.window.title("Edit Task")
        self.window.pack_propagate(False)

        try:
            task_number = ""
            for i in range(3):
                if master["text"][i].isdigit():
                    task_number += master["text"][i]
                else:
                    pass
        except IndexError:
            pass

        task_number = int(task_number) if task_number != "" else 1

        label = Label(self.window, text=f"Edit Task #{task_number}", font="Helvetica 24")
        label.pack(fill=BOTH, pady=(30, 0))

        self.task_text = Text(self.window, font="Verdana 14", height=3)
        self.task_text.insert("1.0", master["text"][4:])
        self.task_text.pack(fill=BOTH, pady=(30, 0))

        set_time = Label(self.window, text="Set/Update time - ", font="Helvetica 16")
        set_time.pack(side=LEFT)

        self.hour_variable = StringVar()
        self.set_hour = Entry(self.window, font="Helvetica 18", width=5, textvariable=self.hour_variable)
        self.set_hour.pack(side=LEFT)
        reg = self.root.register(self.hour_checker)
        self.set_hour.config(validate="key", validatecommand=(reg, "%S", "%P", "%d"))

        match = re.search(" at \d{1,2}", master["text"])
        if match is not None:
            self.task_text.delete(1.0, END)
            self.task_text.insert(1.0, master["text"][4:match.start()])
            time = "".join(filter(str.isdigit, match.group()[-5:]))
            self.set_hour.insert(0, time)

        edit_task_btn = Button(self.window, text="Edit Task", command=lambda: self.edit_task(master),
                               font="Helvetica 12")
        edit_task_btn.pack(side=RIGHT, padx=20)

    def edit_task(self, master):
        time = self.set_hour.get()
        if len(time) == 3:
            time = time[:2]
        elif len(time) == 4:
            time = time[:3] + "0" + time[-1]

        updated_task = self.task_text.get("1.0", "end-1c")
        self.window.destroy()
        if time != "":
            master["text"] = master["text"][:4] + updated_task + " at " + time
        else:
            master["text"] = master["text"][:4] + updated_task
        self.update_images(master)

    def update_tasks(self, task_number, master):
        # function to update the numeration on the tasks if the user deleted a task with other tasks underneath
        for child in master.winfo_children()[1:]:
            if "label" in child.winfo_name() and "#" in child["text"]:
                curr_n = ""
                for i in range(1, 4):
                    if child["text"][i].isdigit():
                        curr_n += child["text"][i]
                    else:
                        end_index = i
                        break
                if int(curr_n) > task_number:
                    self.update_images(child)
                    if curr_n == "2":
                        child.pack(padx=25, pady=(5, 0), fill=BOTH)
                    child["text"] = f"#{int(curr_n) - 1}" + child["text"][end_index:]
                    if curr_n == 2:
                        child.pack(pady=(5, 0))

    def delete_task(self, master):
        if master["text"] != " ":
            try:
                curr_task_num = ""
                for i in range(4):
                    if master["text"][i].isdigit():
                        curr_task_num += master["text"][i]
                curr_task_num = int(curr_task_num)
            except IndexError:
                pass
        else:
            curr_task_num = 0

        number_of_tasks = self.get_task_number(master.master)
        day_frame = master.master
        if curr_task_num < number_of_tasks:
            self.update_tasks(curr_task_num, day_frame)

        if number_of_tasks == 0:
            txt = self.create_empty_label(day_frame)
            txt.pack(padx=25, pady=(5, 0), fill=BOTH)
        else:
            # completed tasks tracker thingy
            day = master.master.winfo_name()[-1]
            if day == "e":
                day = 1
            day = int(day) - 1

            cb = master.winfo_children()[-1]
            state = cb.getvar(cb["variable"])
            if state == 1:
                self.completed_tasks[day] -= 1

        master.destroy()

    def update_images(self, master):
        for child in master.winfo_children():
            child.focus_force()


tm = TaskManager()