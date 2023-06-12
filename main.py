# main.py

import tkinter as tk
from tkinter import filedialog
import joblib
import nltk

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from backup_manager import BackupManager
from model_trainer import ModelTrainer
from file_classifier import FileClassifier

# Ensure the required NLTK data is downloaded
nltk.download('stopwords')

def create_and_configure_widgets(root: tk.Tk, model_trainer: ModelTrainer, file_classifier: FileClassifier, backup_manager: BackupManager):
    """Create and configure tkinter widgets.
    
    Args:
        root (tk.Tk): The tkinter root window.
        model_trainer (ModelTrainer): An instance of the ModelTrainer class.
        file_classifier (FileClassifier): An instance of the FileClassifier class.
        backup_manager (BackupManager): An instance of the BackupManager class.
    """
    train_button = tk.Button(root, text="Train a New Model", command=model_trainer.train_model)
    classify_button = tk.Button(root, text="Organize Desktop", command=file_classifier.classify_files)
    load_button = tk.Button(root, text="Load a Model", command=file_classifier.load_model)
    select_button = tk.Button(root, text="Select a Model", command=file_classifier.select_model)
    backup_button = tk.Button(root, text="Backup Desktop", command=backup_manager.make_backup)
    restore_button = tk.Button(root, text="Restore Desktop", command=backup_manager.restore_backup)
    model_trainer.model_list = tk.Listbox(root)

    # Use grid layout for better control over placement of widgets
    train_button.grid(row=0, column=0, sticky='w')
    classify_button.grid(row=1, column=0, sticky='w')
    load_button.grid(row=2, column=0, sticky='w')
    select_button.grid(row=3, column=0, sticky='w')
    backup_button.grid(row=4, column=0, sticky='w')
    restore_button.grid(row=5, column=0, sticky='w')
    model_trainer.model_list.grid(row=0, column=1, rowspan=6, sticky='nsew')

    # Configure grid to expand correctly when window is resized
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(5, weight=1)

def main():
    """Main function to set up and start the tkinter GUI."""

    backup_manager = BackupManager()
    model_trainer = ModelTrainer()
    file_classifier = FileClassifier()

    root = tk.Tk()
    root.title("Desktop Organizer")

    create_and_configure_widgets(root, model_trainer, file_classifier, backup_manager)

    root.mainloop()

if __name__ == "__main__":
    main()
