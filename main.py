import os
import shutil
import joblib
import nltk
import magic
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime

nltk.download('stopwords')

# Get the list of stopwords
stopwords = set(stopwords.words('english'))

# Create the CountVectorizer
vectorizer = CountVectorizer(stop_words=stopwords)

# Create the GUI
root = tk.Tk()

# Create the model variable and models list
model = tk.StringVar()
models = []

# Create backup directory path
backup_dir = os.path.expanduser("~/Desktop_backup")

# Function to make a backup
def make_backup():
    desktop = os.path.expanduser("~/Desktop")
    if not os.path.exists(backup_dir):
        shutil.copytree(desktop, backup_dir)
    else:
        messagebox.showinfo("Error", "Backup already exists!")

# Function to restore from a backup
def restore_backup():
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(backup_dir):
        shutil.rmtree(desktop)
        shutil.copytree(backup_dir, desktop)
    else:
        messagebox.showinfo("Error", "No backup found!")

# Function to train a model
def train_model():
    dir_path = filedialog.askdirectory()
    
    if not dir_path:
        return

    subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

    if not subdirs:
        messagebox.showinfo("Error", "No subdirectories found!")
        return
    
    texts = []
    labels = []
    
    for subdir in subdirs:
        files = os.listdir(os.path.join(dir_path, subdir))
        for file in files:
            with open(os.path.join(dir_path, subdir, file), 'r') as f:
                texts.append(f.read())
                labels.append(get_label(os.path.join(dir_path, subdir)))
    
    X = vectorizer.fit_transform(texts)
    new_model = MultinomialNB().fit(X, labels)
    models.append(new_model)
    model_list.insert(tk.END, f"Model {len(models)}")

# Function to ask the user for a label for each subdirectory
def get_label(dir_path):
    label = simpledialog.askstring("Input", f"Enter label for {dir_path}")
    return label

# Function to classify and move files
def classify_files():
    if model.get() == '':
        messagebox.showinfo("Error", "No model loaded!")
        return

    path = os.path.expanduser("~/Desktop")
    files = os.listdir(path)
    mime = magic.Magic(mime=True)
    
    for file in files:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            continue
        
        mimetype = mime.from_file(filepath)
        if "text" in mimetype:
            with open(filepath, 'r') as f:
                text = f.read()
                features = vectorizer.transform([text])
                label = model.get().predict(features)
                
                date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')
                new_dir = os.path.join(path, label[0], date)
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                
                shutil.move(filepath, new_dir)

# Function to load a model
def load_model():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        model.set(joblib.load(file_path))
    except:
        messagebox.showinfo("Error", "Failed to load the model!")

# Function to select a model
def select_model():
    selected_index = model_list.curselection()[0]
    model.set(models[selected_index])

# Create the buttons and listbox
train_button = tk.Button(root, text="Train a New Model", command=train_model)
classify_button = tk.Button(root, text="Organize Desktop", command=classify_files)
load_button = tk.Button(root, text="Load a Model", command=load_model)
select_button = tk.Button(root, text="Select a Model", command=select_model)
backup_button = tk.Button(root, text="Backup Desktop", command=make_backup)
restore_button = tk.Button(root, text="Restore Desktop", command=restore_backup)
model_list = tk.Listbox(root)

train_button.pack()
classify_button.pack()
load_button.pack()
select_button.pack()
model_list.pack()
backup_button.pack()
restore_button.pack()

# Start the GUI
root.mainloop()
