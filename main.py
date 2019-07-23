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
        root.title("Celaria Map Converter")
        root.resizable(False, False)
        root.geometry("220x160")
        root.iconbitmap("cmc.ico")

        # Buttons
        self.save_button = Button(root, text="Save File", command=self.save_file, height=1, width=9, state="disabled")
        self.save_button.place(x=136, y=125)

        self.open_button = Button(root, text="Open File", command=self.open_file, height=1, width=9, state="normal")
        self.open_button.place(x=10, y=125)

        self.downgrade_button = Button(root, text="Downgrade map", command=self.downgrade, height=1, width=12,
                                       state="disabled")
        self.downgrade_button.place(x=115, y=90)

        self.upgrade_button = Button(root, text="Upgrade map", command=self.upgrade, height=1, width=12,
                                     state="disabled")
        self.upgrade_button.place(x=10, y=90)

        # Labels (Map info for end user pleasure)

        self.map_name_label = Label(root, height=1, text="Map name: ")
        self.map_name_label_changing = Label(root, height=1, text="No map loaded")
        self.map_name_label.place(x=10, y=10)
        self.map_name_label_changing.place(x=75, y=10)

        self.map_version_label = Label(root, height=1, text="Map version:")
        self.map_version_label_changing = Label(root, height=1, text="No map loaded")
        self.map_version_label.place(x=10, y=35)
        self.map_version_label_changing.place(x=85, y=35)

        self.map_entity_count_label = Label(root, height=1, text="Map entity count:")
        self.map_entity_count_label_changing = Label(root, height=1, text="No map loaded")
        self.map_entity_count_label.place(x=10, y=60)
        self.map_entity_count_label_changing.place(x=110, y=60)

        root.mainloop()
    
    def save_file(self):
        cmt.encode(self.cmap, Path(filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(
            ("Celaria map files", "*.cmap"), ("All files", "*.*"))) + ".cmap"))

    def open_file(self):
        opened_file = filedialog.askopenfilename(initialdir="/", title="Open file",
                                                 filetypes=(("Celaria map files", "*.cmap"), ("All files", "*.*")))

		try:
			self.cmap = cmt.decode(Path(opened_file))
		except ValueError as err:
			messagebox.showerror("Decoder error", str(err))
			return

        self.save_button['state'] = "disabled"

        self.map_name_label_changing['text'] = self.cmap.name
        self.map_version_label_changing['text'] = self.cmap.format_version
        self.map_entity_count_label_changing['text'] = len(self.cmap.entities)

        if self.cmap.format_version == 1:
            self.upgrade_button['state'] = "disabled"
            self.downgrade_button['state'] = "normal"
        elif self.cmap.format_version == 0:
            self.downgrade_button['state'] = "disabled"
            self.upgrade_button['state'] = "normal"

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
        self.map_version_label_changing['text'] = self.cmap.format_version


MyGui()
