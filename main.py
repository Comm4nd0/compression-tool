#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory

import subprocess
import configparser

FILES = []
COMPRESS_TYPE = ['zip', 'tar.gz']

class Choices(ScrolledText):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, cursor="arrow", **kwargs)
        self.item_id = {}
        self.create_files_window(master)

    def create_files_window(self, master):
        var = 0
        for file in FILES:
            self.item_id[var] = tk.BooleanVar(master)
            check_box = tk.Checkbutton(self, text=file, variable=self.item_id[var], bg='#999999', fg='#222222', selectcolor='#ffffff', borderwidth=3, highlightthickness=0)
            self.window_create(tk.END, window=check_box, )
            self.insert(tk.END, '\n')
            var += 1

        self.config(state=tk.DISABLED, width=65, height=17, background='#999999')


class GUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.center(500, 425)
        self.master.configure(background='#333333')
        self.master.title("Compression Tool")

        # causes the full width of the window to be used
        self.columnconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)
        self.make_UI()

    def make_UI(self):
        style = ttk.Style()
        # global style changes
        style.configure(".", background='#333333', foreground='white', anchor="center")
        # Button style changes
        style.map("TButton", background=[('active', 'orange'), ('hover', '#222222')])
        style.map("TMenubutton", background=[('hover', '#222222')])
        style.map("TEntry", foreground=[('focus', 'blue2'), ('active', 'green2')])
        style.map("TCheckbutton", background=[('hover', '#222222')])

        heading = ttk.Label(self, text="Compression Tool", font=("Courier", 20))
        heading.grid(column=0, row=1, rowspan=1, columnspan=3, sticky='NWES')

        intro = ttk.Label(self, font=("Courier", 16))
        intro['text'] = "Browse files to compress"
        intro.grid(column=0, row=2, rowspan=1, columnspan=3, sticky='NWES', padx=5, pady=20)

        self.browse_files = ttk.Button(self, text="Add Files", command=self.load_files, width=10, state='active')
        #self.browse_files.config['backgound'] = '#ffffff'
        self.browse_files.grid(column=0, row=3, rowspan=1, columnspan=1, sticky='N', padx=5, pady=5)

        self.files_window = Choices(self)
        self.files_window.grid(column=0, row=4, columnspan=3, sticky='N', padx=5, pady=5)

        #self.compress_option = tk.StringVar(self)
        #self.compress_option.set("Select Type")
        #option = ttk.OptionMenu(self, self.compress_option, "Compression Type", *COMPRESS_TYPE)
        #option.grid(column=2, row=3, sticky='E', padx=5, pady=5)

        self.browse_folder = ttk.Button(self, text="Output Folder", command=self.load_output_dir, width=10, state='active')
        self.browse_folder.grid(column=0, row=5, rowspan=1, columnspan=1, sticky='N', padx=5, pady=5)

        self.output_location = ttk.Label(self, font=("Courier", 12))
        self.output_location['text'] = "No folder selected"
        self.output_location.grid(column=1, row=5, rowspan=1, columnspan=3, sticky='W', padx=5, pady=5)

        self.compress_button = ttk.Button(self, text="Compress", command=self.compress, width=10)
        self.compress_button.grid(column=2, row=5, rowspan=1, columnspan=1, sticky='E', padx=5, pady=5)

        #self.no_files = ttk.Label(self, font=("Courier", 12))
        #self.no_files['text'] = "No files selected"
        #self.no_files.grid(column=0, row=4, rowspan=1, columnspan=3, sticky='NWES', padx=5, pady=20)

        # EXIT
        #exit_button = ttk.Button(self, text="Exit", command=self.exit)
        #exit_button.grid(column=0, row=9, sticky='N')

    def center(self, width, height):
        """center the window on the screen"""
        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def load_files(self):
        self.fnames = askopenfilenames(title='Select files',  initialdir='~/')

        for file in self.fnames:
            if file not in FILES:
                FILES.append(file)

        self.update_file_window()

    def load_output_dir(self):
        self.output_dir = askdirectory(title="Select A Folder", mustexist=1, initialdir='~/')

        output_text = self.output_dir
        if len(self.output_dir) > 26:
            output_text = "..." + self.output_dir[-26:]
        self.output_location['text'] = output_text

    def update_file_window(self):
        self.files_window.destroy()
        self.files_window = Choices(self)
        self.files_window.grid(column=0, row=4, columnspan=3, sticky='N', padx=5, pady=5)

        if len(self.files_window.item_id) >= 1:
            try:
                self.rem_selected.destroy()
            except:
                pass
            self.rem_selected = ttk.Button(self, text="Remove Selected", command=self.remove_selected, width=10)
            self.rem_selected.grid(column=1, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)
        else:
            try:
                self.rem_selected.destroy()
            except:
                pass

    def compress(self):
        print("compress")

    def remove_selected(self):
        files = self.files_window.item_id
        offset = 0
        for item in list(self.files_window.item_id):
            if files[item].get() == True:
                FILES.pop(item - offset)
                offset += 1
                self.files_window.item_id.pop(item)

        self.update_file_window()


    def exit(self):
        quit()


if __name__ == '__main__':
    root = tk.Tk()
    window = GUI(root)
    window.pack(fill=tk.X, expand=True, anchor=tk.N)
root.mainloop()