# main.py

import tkinter as tk
from tkinter import filedialog
import joblib
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('stopwords')

from backup_manager import BackupManager
from model_trainer import ModelTrainer
from file_classifier import FileClassifier

backup_manager = BackupManager()
model_trainer = ModelTrainer()
file_classifier = FileClassifier()

root = tk.Tk()

train_button = tk.Button(root, text="Train a New Model", command=model_trainer.train_model)
classify_button = tk.Button(root, text="Organize Desktop", command=file_classifier.classify_files)
load_button = tk.Button(root, text="Load a Model", command=file_classifier.load_model)
select_button = tk.Button(root, text="Select a Model", command=file_classifier.select_model)
backup_button = tk.Button(root, text="Backup Desktop", command=backup_manager.make_backup)
restore_button = tk.Button(root, text="Restore Desktop", command=backup_manager.restore_backup)
model_trainer.model_list = tk.Listbox(root)

train_button.pack()
classify_button.pack()
load_button.pack()
select_button.pack()
model_trainer.model_list.pack()
backup_button.pack()
restore_button.pack()

root.mainloop()
