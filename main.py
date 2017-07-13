#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
from hurry.filesize import size
import os
import zipfile

ICON = '@zip2.xbm'
FILES = []

class Choices(ScrolledText):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, cursor="arrow", **kwargs)
        self.item_id = {}
        self.create_files_window(master)

    def create_files_window(self, master):
        var = 0
        if len(FILES) > 0:
            total_size = 0

            for file in FILES:
                if os.path.isfile(file):
                    total_size += os.path.getsize(file)
                elif os.path.isdir(file):
                    for root, dirs, files in os.walk(file):
                        for item in files:
                            total_size += os.path.getsize(root + "/" + item)

            topbar_text = str(len(FILES)) + ' items added | ' + str(size(total_size)) + ' Total Size'
            self.topbar = tk.Label(text=topbar_text)
            self.window_create(tk.END, window=self.topbar)
            self.insert(tk.END, '\n')
        for file in FILES:
            self.item_id[var] = tk.BooleanVar(master)
            check_box = tk.Checkbutton(self, text=file, variable=self.item_id[var], bg='#999999', fg='#222222', selectcolor='#ffffff', borderwidth=3, highlightthickness=0)
            self.window_create(tk.END, window=check_box, )
            self.insert(tk.END, '\n')
            var += 1

        self.config(state=tk.DISABLED, width=70, height=17, background='#999999')


class GUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.center('master', 525, 355)
        self.master.configure(background='#333333')
        self.master.title("Compression Tool")
        #img = tk.PhotoImage(file='zip2.xbm')
        self.master.iconbitmap(ICON)
        # causes the full width of the window to be used
        self.columnconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        self.output_dir = ''
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

        self.browse_files = ttk.Button(self, text="Add Files", command=self.load_files, width=10, state='active')
        self.browse_files.grid(column=0, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

        self.browse_folders = ttk.Button(self, text="Add Folders", command=self.load_folders, width=10, state='active')
        self.browse_folders.grid(column=1, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

        self.files_window = Choices(self)
        self.files_window.grid(column=0, row=4, columnspan=3, sticky='N', padx=5, pady=5)

        self.output_button = ttk.Button(self, text="Output Dir", command=self.load_output_dir, width=10, state='active')
        self.output_button.grid(column=0, row=5, rowspan=1, columnspan=1, sticky='N', padx=5, pady=5)

        self.output_location = ttk.Label(self, font=("Courier", 12))
        self.output_location['text'] = "No folder selected"
        self.output_location.grid(column=1, row=5, rowspan=1, columnspan=3, sticky='W', padx=5, pady=5)

        self.compress_button = ttk.Button(self, text="Compress", command=self.compress, width=10, state='disabled')
        self.compress_button.grid(column=2, row=5, rowspan=1, columnspan=1, sticky='E', padx=5, pady=5)

    def center(self, win, width, height):
        """center the window on the screen"""
        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        # set the dimensions of the screen
        # and where it is placed
        if win == 'master':
            self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        if win == 'popup':
            self.top.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def load_files(self):
        self.fnames = askopenfilenames(title='Select files',  initialdir='~/')

        for file in self.fnames:
            if file not in FILES:
                FILES.append(file)

        self.update_file_window()
        self.check_status()

    def load_folders(self):
        folder = askdirectory(title='Select folders', initialdir='~/')
        FILES.append(folder)

        self.update_file_window()
        self.check_status()

    def load_output_dir(self):
        self.output_dir = asksaveasfilename(title="Select A Folder", filetypes = [("zip folder","*.zip")], initialdir='~/')

        output_text = self.output_dir
        if len(self.output_dir) > 28:
            output_text = "..." + self.output_dir[-28:]
        self.output_location['text'] = output_text
        self.check_status()

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
            self.rem_selected.grid(column=2, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)
        else:
            try:
                self.rem_selected.destroy()
            except:
                pass

    def compress(self):
        print("compress")
        print(FILES)
        print("Output dir: " + self.output_dir)

        zip_f = zipfile.ZipFile(self.output_dir, 'w')
        for item in FILES:
            if os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for filename in files:
                        zip_f.write(os.path.join(root, filename))
            elif os.path.isfile(item):
                zip_f.write(item)
        zip_f.close()
        self.confirm()

    def confirm(self):
        self.top = tk.Toplevel()
        self.send_email = tk.IntVar()
        self.center('popup', 190, 100)
        self.top.iconbitmap(ICON)
        if os.path.isfile(self.output_dir):
            self.center('popup', 190, 100)
            self.top.title("Success!")
            msg = tk.Label(self.top, text='Zip file created successfully!')
            msg.grid(column=1, row=1, rowspan=1, columnspan=2, sticky='WENS', padx=5, pady=5)
            email = tk.Checkbutton(self.top, text="Send via email?", variable=self.send_email)
            email.grid(column=1, row=2, rowspan=1, columnspan=2, sticky='WENS', padx=5, pady=5)
            exit = tk.Button(self.top, text="Exit", command=self.exit)
            exit.grid(column=1, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)
            cont = tk.Button(self.top, text="Continue", command=self.send_mail)
            cont.grid(column=2, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

        else:
            self.center('popup', 250, 100)
            self.top.title("Failure to create Zip file")
            msg = tk.Label(self.top, text='Check that you have permission to ' + self.output_dir, wraplength=250)
            msg.grid(column=1, row=1, rowspan=1, columnspan=2, sticky='WENS', padx=5, pady=5)
            exit = tk.Button(self.top, text="Exit", command=self.exit)
            exit.grid(column=1, row=2, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)
            cont = tk.Button(self.top, text="Continue", command=self.top.destroy)
            cont.grid(column=2, row=2, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

    def remove_selected(self):
        files = self.files_window.item_id
        offset = 0
        for item in list(self.files_window.item_id):
            if files[item].get() == True:
                FILES.pop(item - offset)
                offset += 1
                self.files_window.item_id.pop(item)

        self.update_file_window()
        self.check_status()

    def check_status(self):
        filename, file_extension = os.path.splitext(self.output_dir)
        if len(FILES) > 0 and file_extension == ".zip":
            self.compress_button.config(state='active')
        else:
            self.compress_button.config(state='disabled')

    def send_mail(self):
        if self.send_email.get():
            command = 'thunderbird -compose attachment="' + self.output_dir + '"'
            os.system(command)
        self.top.destroy()

    def exit(self):
        self.send_mail()
        quit()


if __name__ == '__main__':
    root = tk.Tk()
    window = GUI(root)
    window.pack(fill=tk.X, expand=True, anchor=tk.N)
    root.mainloop()