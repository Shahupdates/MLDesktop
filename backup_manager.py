# backup_manager.py

import os
import shutil
import tkinter.messagebox as messagebox

class BackupManager:
    def __init__(self):
        self.backup_dir = os.path.expanduser("~/Desktop_backup")

    def make_backup(self):
        desktop = os.path.expanduser("~/Desktop")
        if not os.path.exists(self.backup_dir):
            shutil.copytree(desktop, self.backup_dir)
        else:
            messagebox.showinfo("Error", "Backup already exists!")

    def restore_backup(self):
        desktop = os.path.expanduser("~/Desktop")
        if os.path.exists(self.backup_dir):
            shutil.rmtree(desktop)
            shutil.copytree(self.backup_dir, desktop)
        else:
            messagebox.showinfo("Error", "No backup found!")
