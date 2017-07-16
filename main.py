#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
from hurry.filesize import size
import filelist
import settings
import os
import zipfile

# the GUI main class
class GUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        settings.init()
        width, height, x, y = settings.center(master, 'master', 525, 355)
        master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.master.configure(background='#333333')
        self.master.title("Compression Tool")
        img = tk.Image("photo", file=settings.ICON)
        self.tk.call('wm','iconphoto',root._w,img)
        # causes the full width of the window to be used
        self.columnconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        self.output_dir = ''
        self.make_UI()

    # Generate the UI and set some global styles
    def make_UI(self):
        style = ttk.Style()
        # global style changes
        style.configure(".", background='#333333', foreground='orange', anchor="center")
        style.map("TButton", background=[('hover', '#222222')])
        style.map("TMenubutton", background=[('hover', '#222222')])
        style.map("TEntry", foreground=[('focus', 'blue2'), ('active', 'green2')])
        style.map("TCheckbutton", background=[('hover', '#222222')])

        heading = ttk.Label(self, text="Compression Tool", font=("Courier", 20))
        heading.grid(column=0, row=1, rowspan=1, columnspan=3, sticky='NWES')

        self.browse_files = ttk.Button(self, text="Add Files", command=self.load_files, width=10, state='active')
        self.browse_files.grid(column=0, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

        self.browse_folders = ttk.Button(self, text="Add Folders", command=self.load_folders, width=10, state='active')
        self.browse_folders.grid(column=1, row=3, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

        self.files_window = filelist.Choices(self)
        self.files_window.grid(column=0, row=4, columnspan=3, sticky='N', padx=5, pady=5)

        self.output_button = ttk.Button(self, text="Save As", command=self.load_output_dir, width=10, state='active')
        self.output_button.grid(column=0, row=5, rowspan=1, columnspan=1, sticky='N', padx=5, pady=5)

        self.output_location = ttk.Label(self, font=("Courier", 12))
        self.output_location['text'] = "No folder selected"
        self.output_location.grid(column=1, row=5, rowspan=1, columnspan=3, sticky='W', padx=5, pady=5)

        self.compress_button = ttk.Button(self, text="Compress", command=self.compress, width=10, state='disabled')
        self.compress_button.grid(column=2, row=5, rowspan=1, columnspan=1, sticky='E', padx=5, pady=5)

    # ask user to browse files then append them to the global FILES var
    def load_files(self):
        self.fnames = askopenfilenames(title='Select files',  initialdir='~/')

        for file in self.fnames:
            if file not in settings.FILES:
                settings.FILES.append(file)

        self.update_file_window()
        self.check_status()

    # Ask user for folders then append to the global FILES var
    def load_folders(self):
        self.folder = askdirectory(title='Select folder', initialdir='~/')
        if self.folder not in settings.FILES and self.folder:
            settings.FILES.append(self.folder)

            self.update_file_window()
            self.check_status()

    # Ask user where to save the zip folder that will be created
    def load_output_dir(self):
        self.output_dir = asksaveasfilename(title="Select A Folder", filetypes = [("zip folder","*.zip")], initialdir='~/')

        output_text = self.output_dir
        if len(self.output_dir) > 28:
            output_text = "..." + self.output_dir[-28:]
        self.output_location['text'] = output_text
        self.check_status()

    # Destroy and create the file window with and changes made
    def update_file_window(self):
        self.files_window.destroy()
        self.files_window = filelist.Choices(self)
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

    # Create the zip file
    def compress(self):
        zip_f = zipfile.ZipFile(self.output_dir, 'w', zipfile.ZIP_DEFLATED)
        for item in settings.FILES:
            if os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for filename in files:
                        zip_f.write(os.path.join(root, filename))
            elif os.path.isfile(item):
                zip_f.write(item, os.path.basename(item))
        zip_f.close()
        self.confirm()

    # Generate a popup window the the result of the created zip folder
    def confirm(self):
        self.top = tk.Toplevel()
        self.send_email = tk.IntVar()
        self.top.lift(aboveThis=root)
        img = tk.Image("photo", file=settings.ICON)
        self.tk.call('wm', 'iconphoto', root._w, img)
        if os.path.isfile(self.output_dir):
            width, height, x, y = settings.center(self.top, 'popup', 190, 125)
            self.top.geometry('%dx%d+%d+%d' % (width, height, x, y))
            self.top.title("Success!")
            msg = tk.Label(self.top, text='Zip file created successfully!')
            msg.grid(column=1, row=1, rowspan=1, columnspan=2, sticky='WENS', padx=5, pady=5)
            res_text = "Before: " + str(size(self.files_window.total_size)) + " After: " + str(size(os.path.getsize(self.output_dir)))
            results = tk.Label(self.top, text=res_text)
            results.grid(column=1, row=2, rowspan=1, columnspan=2, sticky='WENS', padx=5, pady=5)
            email = tk.Checkbutton(self.top, text="Send via email?", variable=self.send_email)
            email.grid(column=1, row=3, rowspan=1, columnspan=2, sticky='WENS', padx=5, pady=5)
            exit = tk.Button(self.top, text="Exit", command=self.exit)
            exit.grid(column=1, row=4, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)
            cont = tk.Button(self.top, text="Continue", command=self.send_mail)
            cont.grid(column=2, row=4, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

        else:
            width, height, x, y = settings.center(self.top, 'popup', 250, 100)
            self.top.geometry('%dx%d+%d+%d' % (width, height, x, y))
            self.top.title("Failure to create Zip file")
            msg = tk.Label(self.top, text='Check that you have permission to ' + self.output_dir, wraplength=250)
            msg.grid(column=1, row=1, rowspan=1, columnspan=2, sticky='WENS', padx=5, pady=5)
            exit = tk.Button(self.top, text="Exit", command=self.exit)
            exit.grid(column=1, row=2, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)
            cont = tk.Button(self.top, text="Continue", command=self.top.destroy)
            cont.grid(column=2, row=2, rowspan=1, columnspan=1, sticky='WENS', padx=5, pady=5)

    # Remove the ticked items from the files window
    def remove_selected(self):
        files = self.files_window.item_id
        offset = 0
        for item in list(self.files_window.item_id):
            if files[item].get() == True:
                settings.FILES.pop(item - offset)
                offset += 1
                self.files_window.item_id.pop(item)

        self.update_file_window()
        self.check_status()

    # Check the GUI state to decide if all the relevant information has been entered
    def check_status(self):
        filename, file_extension = os.path.splitext(self.output_dir)
        if len(settings.FILES) > 0 and file_extension == ".zip":
            self.compress_button.config(state='alternate')
        else:
            self.compress_button.config(state='disabled')

    # Open Thunderbird attach the zip folder to a new mail
    def send_mail(self):
        if self.send_email.get():
            command = '/usr/bin/thunderbird -compose attachment="' + self.output_dir + '" &'
            os.system(command)
        self.top.destroy()

    # exit the program
    def exit(self):
        self.send_mail()
        quit()

if __name__ == '__main__':
    root = tk.Tk()
    window = GUI(root)
    window.pack(fill=tk.X, expand=True, anchor=tk.N)
    root.mainloop()