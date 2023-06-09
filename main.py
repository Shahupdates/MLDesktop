import os
import shutil
import joblib
import nltk
import tkinter as tk
from tkinter import filedialog
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from filetype import guess

nltk.download('stopwords')

# Get the list of stopwords
stopwords = set(stopwords.words('english'))

# Create the CountVectorizer
vectorizer = CountVectorizer(stop_words=stopwords)

# Create the GUI
root = tk.Tk()

# Create the model variable
model = tk.StringVar()

def train_model():
    # Ask the user to select a directory
    dir_path = filedialog.askdirectory()
    
    # Get the list of all subdirectories
    subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    
    # Create lists to store the file contents and their labels
    texts = []
    labels = []
    
    # Load the files
    for subdir in subdirs:
        files = os.listdir(os.path.join(dir_path, subdir))
        for file in files:
            with open(os.path.join(dir_path, subdir, file), 'r') as f:
                texts.append(f.read())
                labels.append(subdir)
    
    # Convert the texts into feature vectors
    X = vectorizer.fit_transform(texts)
    
    # Train the model
    model.set(MultinomialNB().fit(X, labels))
    
    # Save the model to a file
    joblib.dump(model.get(), 'model.joblib')

def classify_files():
    # Check if a model is loaded
    if model.get() == '':
        print("No model loaded!")
        return
    
    # Ask the user to select a directory
    dir_path = filedialog.askdirectory()
    
    # Get the list of all files in the directory
    files = os.listdir(dir_path)
    
    for file in files:
        filepath = os.path.join(dir_path, file)
        
        # Check if the file is a text file
        kind = guess(filepath)
        
        if kind is None:
            print(f"Cannot guess file type for {file}!")
            continue

        if "text" in kind.mime:
            with open(filepath, 'r') as f:
                text = f.read()
                features = vectorizer.transform([text])
                label = model.get().predict(features)
                
                # Create the directory if it doesn't already exist
                new_dir = os.path.join(dir_path, label[0])
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                
                # Move the file
                shutil.move(filepath, new_dir)

def load_model():
    # Ask the user to select a file
    file_path = filedialog.askopenfilename()
    
    # Load the model from the file
    model.set(joblib.load(file_path))

# Create the buttons
train_button = tk.Button(root, text="Train a New Model", command=train_model)
classify_button = tk.Button(root, text="Classify Files", command=classify_files)
load_button = tk.Button(root, text="Load a Model", command=load_model)

train_button.pack()
classify_button.pack()
load_button.pack()

# Start the GUI
root.mainloop()
