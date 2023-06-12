from pathlib import Path
import shutil
import tkinter.messagebox as messagebox

class BackupManager:
    def __init__(self):
        """Initialize the backup directory."""
        self.backup_dir = Path.home() / "Desktop_backup"

    def make_backup(self):
        """Create a backup of the desktop."""
        desktop = Path.home() / "Desktop"

        if not self.backup_dir.exists():
            try:
                shutil.copytree(desktop, self.backup_dir)
                messagebox.showinfo("Success", "Backup created successfully!")
            except Exception as e:
                messagebox.showinfo("Error", f"Failed to create backup! Error: {e}")
        else:
            messagebox.showinfo("Error", "Backup already exists!")

    def restore_backup(self):
        """Restore the desktop from the backup."""
        desktop = Path.home() / "Desktop"

        if self.backup_dir.exists() and any(self.backup_dir.iterdir()):
            if messagebox.askyesno("Confirm Restore", "Are you sure you want to restore the backup? This will replace all current files on the desktop."):
                try:
                    shutil.rmtree(desktop)
                    shutil.copytree(self.backup_dir, desktop)
                    messagebox.showinfo("Success", "Desktop restored successfully!")
                except Exception as e:
                    messagebox.showinfo("Error", f"Failed to restore backup! Error: {e}")
        else:
            messagebox.showinfo("Error", "No backup found!")
