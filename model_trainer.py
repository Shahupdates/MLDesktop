import os
from typing import Set, List
from pathlib import Path
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
    def get_stopwords() -> Set[str]:
        """Get English stopwords.

        Returns:
            set: A set of stopwords.
        """
        return set(stopwords.words('english'))

    def train_model(self):
        """Train a new model using texts from a directory selected by the user."""
        dir_path = Path(filedialog.askdirectory())
        
        if not dir_path.is_dir():
            return

        subdirs = [d for d in dir_path.iterdir() if d.is_dir()]

        if not subdirs:
            messagebox.showinfo("Error", "No subdirectories found!")
            return
        
        texts, labels = self.get_texts_and_labels(subdirs)

        X = self.vectorizer.fit_transform(texts)
        new_model = MultinomialNB().fit(X, labels)
        self.models.append(new_model)
        self.model_list.insert(tk.END, f"Model {len(self.models)}")

    def get_texts_and_labels(self, subdirs: List[Path]) -> tuple:
        """Get texts from files and their labels.

        Args:
            subdirs (list): A list of subdirectories.

        Returns:
            tuple: A tuple of two lists (texts and labels).
        """
        texts = []
        labels = []
        
        for subdir in subdirs:
            files = subdir.iterdir()
            for file in files:
                try:
                    with open(file, 'r') as f:
                        texts.append(f.read())
                        labels.append(self.get_label(subdir))
                except Exception as e:
                    messagebox.showinfo("Error", f"Could not open file {file}. Error: {e}")
        
        return texts, labels

    @staticmethod
    def get_label(dir_path: Path) -> str:
        """Ask user to input a label for a directory.

        Args:
            dir_path (Path): A path to a directory.

        Returns:
            str: A label for a directory.
        """
        label = simpledialog.askstring("Input", f"Enter label for {dir_path}")
        while not label:
            messagebox.showinfo("Error", "Label cannot be empty.")
            label = simpledialog.askstring("Input", f"Enter label for {dir_path}")
        return label
