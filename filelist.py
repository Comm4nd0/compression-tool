#!/usr/bin/python3

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from hurry.filesize import size
import settings
import os

class Choices(ScrolledText):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, cursor="arrow", **kwargs)
        self.item_id = {}
        self.check_box = {}
        self.total_size = 0
        self.create_files_window(master)

    # Window for displaying files and folders and some header info about the contents
    def create_files_window(self, master):
        var = 0

        # get file/folder sizes
        for file in settings.FILES:
            if os.path.isfile(file):
                self.total_size += os.path.getsize(file)
            elif os.path.isdir(file):
                self.total_size += self.iter_dirs(file)
        # insert top bar into window
        topbar_text = str(len(settings.FILES)) + ' items added | ' + str(size(self.total_size)) + ' Total Size'
        self.topbar = tk.Label(text=topbar_text)
        self.window_create(tk.END, window=self.topbar)
        self.insert(tk.END, '\n')

        if len(settings.FILES) > 0:
            # insert all checkbox into window
            self.item_all = tk.BooleanVar(master)
            all_box = tk.Checkbutton(self, text='Select All', variable=self.item_all, bg='#999999', fg='#222222',
                                       selectcolor='#ffffff', borderwidth=3, highlightthickness=0, command=self.toggle_all)
            self.window_create(tk.END, window=all_box, )
            self.insert(tk.END, '\n')

        # insert check boxes, file name and their sizes into window
        for file in settings.FILES:
            self.item_id[var] = tk.BooleanVar(master)
            if os.path.isfile(file):
                text = file + " | " + str(size(os.path.getsize(file)))
            elif os.path.isdir(file):
                self.folder_size = self.iter_dirs(file)
                text = file + " | " + str(size(self.folder_size))
            self.check_box[var] = tk.Checkbutton(self, text=text, variable=self.item_id[var], bg='#999999', fg='#222222', selectcolor='#ffffff', borderwidth=3, highlightthickness=0)
            self.window_create(tk.END, window=self.check_box[var], )
            self.insert(tk.END, '\n')
            var += 1

        self.config(state=tk.DISABLED, width=70, height=17, background='#999999')

    def iter_dirs(self, file):
        size = 0
        for root, dirs, files in os.walk(file):
            for item in files:
                try:
                    size += os.path.getsize(root + "/" + item)
                except FileNotFoundError:
                    self.warning('Unable to add file:\n', item)
        return size

    def toggle_all(self):
        if self.item_all.get() == True:
            for box in self.check_box:
                self.check_box[box].select()
        else:
            for box in self.check_box:
                self.check_box[box].deselect()

    def warning(self, msg_text, item):
        self.top = tk.Toplevel()
        width, height, x, y = settings.center(self.top, 'Warning', 180, 100)
        self.top.geometry('%dx%d+%d+%d' % (width, height, x, y))
        #img = tk.Image("photo", file=settings.ICON)
        #self.tk.call('wm', 'iconphoto', self._w, img)

        self.top.title("Warning!")
        msg = tk.Label(self.top, text=msg_text + item + "\nCheck permissions")
        msg.grid(column=1, row=1, rowspan=1, columnspan=2, sticky='N', padx=5, pady=5)

        cont = tk.Button(self.top, text="Continue", command=self.top.destroy)
        cont.grid(column=1, row=4, rowspan=1, columnspan=1, sticky='N', padx=5, pady=5)