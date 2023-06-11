# model_trainer.py

import os
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

class ModelTrainer:
    def __init__(self):
        self.vectorizer = CountVectorizer(stop_words=self.get_stopwords())
        self.models = []
        self.model_list = None

    @staticmethod
    def get_stopwords():
        return set(stopwords.words('english'))

    def train_model(self):
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
                    labels.append(self.get_label(os.path.join(dir_path, subdir)))
        
        X = self.vectorizer.fit_transform(texts)
        new_model = MultinomialNB().fit(X, labels)
        self.models.append(new_model)
        self.model_list.insert(tk.END, f"Model {len(self.models)}")

    @staticmethod
    def get_label(dir_path):
        label = simpledialog.askstring("Input", f"Enter label for {dir_path}")
        return label
