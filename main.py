from pathlib import Path
from datetime import timedelta

import re

import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import cmt
from cmt.cmap.v1.cmap import CMap


class MyGui:
    def __init__(self):
        self.cmap = CMap()

        root = tkinter.Tk()
        root.title("Celaria Map Info Editor")
        root.resizable(False, False)
        root.geometry("400x300")

        # Buttons

        self.save_button = Button(root, text="Save File", command=self.save_file, height=1, width=9, state="disabled")
        self.save_button.place(x=315, y=265)

        self.open_button = Button(root, text="Open File", command=self.open_file, height=1, width=9, state="normal")
        self.open_button.place(x=15, y=265)

        self.downgrade_button = Button(root, text="Downgrade map", command=self.downgrade, height=1, width=12,
                                       state="disabled")
        self.downgrade_button.place(x=102, y=265)

        self.upgrade_button = Button(root, text="Upgrade map", command=self.upgrade, height=1, width=12,
                                     state="disabled")
        self.upgrade_button.place(x=208, y=265)

        # Labels

        self.name_label = Label(root, text="Map name:", height=1)  # self.cmap.name
        self.name_label.place(x=15, y=15)

        self.sun_rotation_label = Label(root, text="Sun rotation:", height=1)  # self.cmap.sun_rotation
        self.sun_rotation_label.place(x=15, y=40)

        self.sun_angle_label = Label(root, text="Sun angle:", height=1)  # self.cmap.sun_angle
        self.sun_angle_label.place(x=15, y=65)

        self.version_label = Label(root, height=1, text="Map version:")  # self.cmap.format_version
        self.version_label.place(x=15, y=90)
        self.version_label_changing = Label(root, height=1, text="No map loaded")
        self.version_label_changing.place(x=85, y=90)

        self.checkpoint_label = Label(root, height=1, text="Editing Checkpoint:")
        self.checkpoint_label.place(x=15, y=130)

        self.platin_label = Label(root, height=1, text="Platinum time:")
        self.platin_label.place(x=15, y=160)

        self.gold_label = Label(root, height=1, text="Gold time:")
        self.gold_label.place(x=15, y=185)

        self.silver_label = Label(root, height=1, text="Silver time:")
        self.silver_label.place(x=15, y=210)

        self.bronze_label = Label(root, height=1, text="Bronze time:")
        self.bronze_label.place(x=15, y=235)

        # Entries

        self.name_entry_var = StringVar()
        self.name_entry = Entry(root, state="disabled", textvariable=self.name_entry_var, width=50)
        self.name_entry_var.trace('w', lambda *args: self.change_name())
        self.name_entry.place(x=85, y=15)

        self.sun_rotation_entry_var = StringVar()
        self.sun_rotation_entry = Entry(root, state="disabled", textvariable=self.sun_rotation_entry_var, width=49)
        self.sun_rotation_entry_var.trace('w', lambda *args: self.change_sun_rotation())
        self.sun_rotation_entry.place(x=91, y=40)

        self.sun_angle_entry_var = StringVar()
        self.sun_angle_entry = Entry(root, state="disabled", textvariable=self.sun_angle_entry_var, width=51)
        self.sun_angle_entry_var.trace('w', lambda *args: self.change_sun_angle())
        self.sun_angle_entry.place(x=79, y=65)

        # Time entries

        self.platin_entry_var = StringVar()
        self.platin_entry = Entry(root, state="disabled", textvariable=self.platin_entry_var, width=47)
        self.platin_entry_var.set(0)
        self.platin_entry_var.trace('w', lambda *args: self.change_time(0))
        self.platin_entry.place(x=103, y=160)

        self.gold_entry_var = StringVar()
        self.gold_entry = Entry(root, state="disabled", textvariable=self.gold_entry_var, width=51)
        self.gold_entry_var.set(0)
        self.gold_entry_var.trace('w', lambda *args: self.change_time(1))
        self.gold_entry.place(x=79, y=185)

        self.silver_entry_var = StringVar()
        self.silver_entry = Entry(root, state="disabled", textvariable=self.silver_entry_var, width=50)
        self.silver_entry_var.set(0)
        self.silver_entry_var.trace('w', lambda *args: self.change_time(2))
        self.silver_entry.place(x=85, y=210)

        self.bronze_entry_var = StringVar()
        self.bronze_entry = Entry(root, state="disabled", textvariable=self.bronze_entry_var, width=49)
        self.bronze_entry_var.set(0)
        self.bronze_entry_var.trace('w', lambda *args: self.change_time(3))
        self.bronze_entry.place(x=91, y=235)

        # Dropdown menu

        self.checkpoint_chosen = StringVar()
        self.checkpoint_list = ["1"]
        self.checkpoint_chosen.set(self.checkpoint_list[0])
        self.checkpoint_dropdown = OptionMenu(root, self.checkpoint_chosen, *self.checkpoint_list)
        self.checkpoint_dropdown['state'] = "disabled"
        self.checkpoint_chosen.trace('w', lambda *args: self.change_dropdown())
        self.checkpoint_dropdown.place(x=145, y=125)

        root.mainloop()

    def save_file(self):
        cmt.encode(self.cmap, Path(filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(
            ("Celaria map files", "*.cmap"), ("All files", "*.*")))))

    def open_file(self):

        self.name_entry_var.set("")
        self.sun_rotation_entry_var.set("0.00")
        self.sun_angle_entry_var.set("0.00")

        opened_file = filedialog.askopenfilename(initialdir="/", title="Open file",
                                                 filetypes=(("Celaria map files", "*.cmap"), ("All files", "*.*")))
        try:
            self.cmap = cmt.decode(Path(opened_file))
        except ValueError as err:
            messagebox.showerror("Decoder error", str(err))
            return

        self.name_entry['state'] = "normal"
        self.sun_rotation_entry['state'] = "normal"
        self.sun_angle_entry['state'] = "normal"
        self.downgrade_button['state'] = "normal"
        self.upgrade_button['state'] = "normal"
        self.checkpoint_dropdown['state'] = "normal"
        self.platin_entry['state'] = "normal"
        self.gold_entry['state'] = "normal"
        self.silver_entry['state'] = "normal"
        self.bronze_entry['state'] = "normal"

        # Dropdown update
        self.checkpoint_list.clear()
        if self.cmap.format_version == 0:
            for idx in range(len(self.cmap.medal_times)):
                self.checkpoint_list.append(idx + 1)
        elif self.cmap.format_version == 1:
            for idx in range(len(self.cmap.checkpoint_times)):
                self.checkpoint_list.append(idx + 1)
        self.update_dropdown()

        # Set times
        self.checkpoint_chosen.set(self.checkpoint_list[0])
        self.change_time(0)
        self.change_time(1)
        self.change_time(2)
        self.change_time(3)

        self.name_entry_var.set(self.cmap.name)
        self.sun_rotation_entry_var.set(self.cmap.sun_rotation)
        self.sun_angle_entry_var.set(self.cmap.sun_angle)
        self.version_label_changing['text'] = self.cmap.format_version

        self.save_button['state'] = "disabled"

        if self.cmap.format_version == 1:
            self.upgrade_button['state'] = "disabled"
            self.downgrade_button['state'] = "normal"
        elif self.cmap.format_version == 0:
            self.downgrade_button['state'] = "disabled"
            self.upgrade_button['state'] = "normal"

    def change_name(self):
        self.cmap.name = self.name_entry_var.get()
        self.save_button['state'] = "normal"

    def change_sun_rotation(self):
        self.sun_rotation_entry_var.set(self.cmap.sun_rotation)
        self.save_button['state'] = "normal"
        try:
            if float(self.sun_rotation_entry_var.get()):
                self.cmap.sun_rotation = float(self.sun_rotation_entry_var.get()) % 360
        except ValueError:
            messagebox.showerror("Value error",
                                 "The sun rotation must be set as a degree (float) value, such as 0.0000 or 1.234567")
            self.sun_rotation_entry_var.set(self.cmap.sun_rotation)

    def change_sun_angle(self):
        self.sun_angle_entry_var.set(self.cmap.sun_angle)
        self.save_button['state'] = "normal"
        try:
            if float(self.sun_angle_entry_var.get()):
                self.cmap.sun_angle = float(self.sun_angle_entry_var.get()) % 360
        except ValueError:
            messagebox.showerror("Value error",
                                 "The sun angle must be set as a degree (float) value, such as 0.0000 or 1.234567")
            self.sun_angle_entry_var.set(self.cmap.sun_angle)

    def upgrade(self):
        try:
            self.cmap = cmt.convert(self.cmap, self.cmap.format_version + 1, self.cmap.identifier)
        except ValueError as err:
            messagebox.showerror("Converter error", str(err))
        self.check_against_limit()
        self.save_button['state'] = "normal"

    def downgrade(self):
        try:
            self.cmap = cmt.convert(self.cmap, self.cmap.format_version - 1, self.cmap.identifier)
        except ValueError as err:
            messagebox.showerror("Converter error", str(err))
        self.check_against_limit()
        self.save_button['state'] = "normal"

    def check_against_limit(self):
        if self.cmap.format_version == 1:
            self.downgrade_button['state'] = "normal"
            self.upgrade_button['state'] = "disabled"
        elif self.cmap.format_version == 0:
            self.upgrade_button['state'] = "normal"
            self.downgrade_button['state'] = "disabled"
        self.version_label_changing['text'] = self.cmap.format_version

    def change_time(self, time_type):
        if self.platin_entry_var.get() == '' or self.gold_entry_var.get() == '' or self.silver_entry_var.get() == '' or self.bronze_entry_var.get() == '':
            return

        checkpoint_chosen = int(self.checkpoint_chosen.get()) - 1

        platin_time = self.time_to_frames(self.platin_entry_var.get())
        gold_time = self.time_to_frames(self.gold_entry_var.get())
        silver_time = self.time_to_frames(self.silver_entry_var.get())
        bronze_time = self.time_to_frames(self.bronze_entry_var.get())

        if self.cmap.format_version == 0:
            if time_type == 0:
                self.cmap.medal_times[checkpoint_chosen].platin = int(platin_time)
            elif time_type == 1:
                self.cmap.medal_times[checkpoint_chosen].gold = int(gold_time)
            elif time_type == 2:
                self.cmap.medal_times[checkpoint_chosen].silver = int(silver_time)
            elif time_type == 3:
                self.cmap.medal_times[checkpoint_chosen].bronze = int(bronze_time)
        elif self.cmap.format_version == 1:
            if time_type == 0:
                self.cmap.checkpoint_times[checkpoint_chosen].platin = int(platin_time)
            elif time_type == 1:
                self.cmap.checkpoint_times[checkpoint_chosen].gold = int(gold_time)
            elif time_type == 2:
                self.cmap.checkpoint_times[checkpoint_chosen].silver = int(silver_time)
            elif time_type == 3:
                self.cmap.checkpoint_times[checkpoint_chosen].bronze = int(bronze_time)

        self.save_button['state'] = "normal"

    def change_dropdown(self):
        checkpoint_chosen = int(self.checkpoint_chosen.get()) - 1
        if self.cmap.format_version == 0:
            platin_time = self.frames_to_time(self.cmap.medal_times[checkpoint_chosen].platin)
            gold_time = self.frames_to_time(self.cmap.medal_times[checkpoint_chosen].gold)
            silver_time = self.frames_to_time(self.cmap.medal_times[checkpoint_chosen].silver)
            bronze_time = self.frames_to_time(self.cmap.medal_times[checkpoint_chosen].bronze)
            self.platin_entry_var.set(platin_time)
            self.gold_entry_var.set(gold_time)
            self.silver_entry_var.set(silver_time)
            self.bronze_entry_var.set(bronze_time)
        if self.cmap.format_version == 1:
            platin_time = self.frames_to_time(self.cmap.checkpoint_times[checkpoint_chosen].platin)
            gold_time = self.frames_to_time(self.cmap.checkpoint_times[checkpoint_chosen].gold)
            silver_time = self.frames_to_time(self.cmap.checkpoint_times[checkpoint_chosen].silver)
            bronze_time = self.frames_to_time(self.cmap.checkpoint_times[checkpoint_chosen].bronze)
            self.platin_entry_var.set(platin_time)
            self.gold_entry_var.set(gold_time)
            self.silver_entry_var.set(silver_time)
            self.bronze_entry_var.set(bronze_time)

    def update_dropdown(self):
        menu = self.checkpoint_dropdown["menu"]
        menu.delete(0, "end")
        for string in self.checkpoint_list:
            menu.add_command(label=string,
                             command=lambda value=string: self.checkpoint_chosen.set(value))

    def frames_to_time(self, frame_count):
        if self.cmap.format_version == 0:
            time = str(timedelta(milliseconds=frame_count * (5/3) * 10))[2:-4]
        elif self.cmap.format_version > 0:
            time = str(timedelta(milliseconds=frame_count * 10))[2:-4]
        return time

    def time_to_frames(self, time):
        time = self.parse_time(time)
        if self.cmap.format_version == 0:
            frame_count = int(time / (5 / 3))
        elif self.cmap.format_version > 0:
            frame_count = time
        return frame_count

    def parse_time(self, time):
        trailing_zeroes = self.count_trailing_zeroes(time[7:8])

        time = timedelta(minutes=int(time[0:2]), seconds=int(time[3:5]), microseconds=int(time[6:8]) * 10000)
        time_total = time.total_seconds()

        trailing_zeroes_total = self.count_trailing_zeroes(str(time_total))
        time_total = int(str(time_total).replace(".", ""))

        if trailing_zeroes == 1 or trailing_zeroes_total == 1:
            time_total = int(str(time_total) + "0")

        return time_total

    def count_trailing_zeroes(self, text):
        return len(text) - len(text.rstrip("0"))

MyGui()
