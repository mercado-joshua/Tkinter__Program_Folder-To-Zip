#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser as cc , Menu, Spinbox, scrolledtext as st, messagebox as mb, filedialog as fd

import zipfile
import os

#===========================
# Main App
#===========================

class App(tk.Tk):
    """Main Application."""

    #===========================================
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_UI()

    #===========================================
    def init_config(self):
        self.resizable(True, True)
        self.title('Backup Folder to Zip Version 1.0')
        self.iconbitmap('python.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    def init_UI(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        button = ttk.Button(self.main_frame, text=f'Browse Folder to Zip', command=self.folder_to_zip)
        button.pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

    # INSTANCE METHODS -------------------------
    def folder_to_zip(self):
        """Back up the entire contents of 'folder' into a ZIP file."""
        folder_path = fd.askdirectory() # make sure folder is absolute

        if folder_path:
            # Figure out the filename this code should use based on what files already exist.
            number = 1
            while True:
                zip_filename = f'{os.path.basename(folder_path)}_{str(number)}.zip'
                if not os.path.exists(zip_filename):
                    break
                number = number + 1

            # Create the ZIP file.
            print(f'Creating {zip_filename}...')
            backup_zip = zipfile.ZipFile(zip_filename, 'w')

            # Walk the entire folder tree and compress the files in each folder.
            for foldername, subfolders, filenames in os.walk(folder_path):
                print(f'Adding files in {foldername}...')

                # Add the current folder to the ZIP file.
                backup_zip.write(foldername)

                # Add all the files in this folder to the ZIP file.
                for filename in filenames:
                    new_basename = f'{os.path.basename(folder_path)}_'
                    if filename.startswith(new_basename) and filename.endswith('.zip'):
                        continue # don't back up the backup ZIP files
                    backup_zip.write(os.path.join(foldername, filename))
            backup_zip.close()
            print('Done.')

            mb.showinfo('Info', 'Done')


#===========================
# Start GUI
#===========================

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()