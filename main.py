import tkinter
from pathlib import Path
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
        root.geometry("400x200")

        # Buttons

        self.save_button = Button(root, text="Save File", command=self.save_file, height=1, width=9, state="disabled")
        self.save_button.place(x=315, y=160)

        self.open_button = Button(root, text="Open File", command=self.open_file, height=1, width=9, state="normal")
        self.open_button.place(x=15, y=160)

        self.downgrade_button = Button(root, text="Downgrade map", command=self.downgrade, height=1, width=12,
                                       state="disabled")
        self.downgrade_button.place(x=102, y=160)

        self.upgrade_button = Button(root, text="Upgrade map", command=self.upgrade, height=1, width=12,
                                     state="disabled")
        self.upgrade_button.place(x=208, y=160)

        # Labels

        self.name_label = Label(root, text="Map name:", height=1) #self.cmap.name
        self.name_label.place(x=15, y=15)

        self.sun_rotation_label = Label(root, text="Sun rotation:", height=1) #self.cmap.sun_rotation
        self.sun_rotation_label.place(x=15, y=40)

        self.sun_angle_label = Label(root, text="Sun angle:", height=1) #self.cmap.sun_angle
        self.sun_angle_label.place(x=15, y=65)

        self.version_label = Label(root, height=1, text="Map version:") #self.cmap.format_version
        self.version_label.place(x=15, y=90)
        self.version_label_changing = Label(root, height=1, text="No map loaded")
        self.version_label_changing.place(x=85, y=90)

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

        root.mainloop()

    def save_file(self):
        cmt.encode(self.cmap, Path(filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(
            ("Celaria map files", "*.cmap"), ("All files", "*.*"))) + ".cmap"))

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
        self.cmap.sun_rotation = self.sun_rotation_entry_var.get()
        self.save_button['state'] = "normal"
        try:
            if float(self.sun_rotation_entry_var.get()):
                self.cmap.sun_angle = float(self.sun_rotation_entry_var.get()) % 360
        except ValueError:
            messagebox.showerror("Value error", "The sun angle must be set as a degree (float) value, such as 0.0000 or 1.234567")
            self.sun_rotation_entry_var.set(self.cmap.sun_angle)
        print("lol1"
    def change_sun_angle(self):
        self.cmap.sun_angle = self.sun_angle_entry_var.get()
        self.save_button['state'] = "normal"
        try:
            if float(self.sun_angle_entry_var.get()):
                self.cmap.sun_angle = float(self.sun_angle_entry_var.get()) % 360
        except ValueError:
            messagebox.showerror("Value error", "The sun angle must be set as a degree (float) value, such as 0.0000 or 1.234567")

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

MyGui()
