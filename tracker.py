from tkinter import *
from tkinter import ttk


class Tracker:
    progress_bars = []
    def __init__(self, master, weekday_tasks, completed_tasks):
        if len(master.winfo_children()) == 0:
            title = Label(master, text="Task Tracker", font="Helvetica 48", bg="#dbd9d9").pack(pady=(110, 60))
            for idx, day in enumerate(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")):
                container = Frame(master, bg="#dbd9d9")
                container.pack()

                textf = Frame(container, bg="#dbd9d9")
                textf.pack(side=LEFT, anchor=W)
                pf = Frame(container, bg="#dbd9d9")
                pf.pack(side=LEFT, anchor=E)

                padx = (0, 0)
                padx_l = 25
                test = 0
                if idx == 0:
                    padx = (10, 10)
                elif idx == 1:
                    padx = (0, 10)
                elif idx == 2:
                    test = (10, 45)
                elif idx == 3:
                    padx = (0, 5)
                    test = (5, 15)
                elif idx == 4:
                    padx = (20, 0)
                    test = (10, 0)
                elif idx == 5:
                    padx = (0, 10)
                    test = (0, 15)
                elif idx == 6:
                    padx = 0
                    test = (10, 0)

                text = Label(textf, text=day, font="Helvetica 20", bg="#dbd9d9").pack(side=LEFT, pady=(0, 25), padx=padx_l, anchor=W)
                value = 100 * (completed_tasks[idx] / weekday_tasks[idx]) if weekday_tasks[idx] != 0 else 0
                pb = ttk.Progressbar(pf, orient=HORIZONTAL, length=200, mode="determinate", value=value)
                pb.pack(side=RIGHT, pady=(0, 25), padx=padx, anchor=E)
                completed_out_of_all = Label(container, font="Helvetica 12", text=f"{completed_tasks[idx]}/{weekday_tasks[idx]}", bg="#dbd9d9")
                completed_out_of_all.pack(side=LEFT, padx=test, pady=(0, 25))

                self.progress_bars.append((pb, completed_out_of_all))
        else:
            for i, (pb, label) in enumerate(self.progress_bars):
                value = 100 * (completed_tasks[i] / weekday_tasks[i]) if weekday_tasks[i] != 0 else 0
                pb["value"] = value
                label["text"] = f"{completed_tasks[i]} / {weekday_tasks[i]}"