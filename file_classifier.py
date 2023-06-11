# file_classifier.py

import os
import shutil
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import magic
from datetime import datetime

class FileClassifier:
    def __init__(self):
        self.model = None

    def classify_files(self):
        if self.model is None:
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
                    features = self.model.vectorizer.transform([text])
                    label = self.model.predict(features)
                    
                    date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')
                    new_dir = os.path.join(path, label[0], date)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    
                    shutil.move(filepath, new_dir)

    def load_model(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        try:
            self.model = joblib.load(file_path)
        except:
            messagebox.showinfo("Error", "Failed to load the model!")

    def select_model(self):
        selected_index = self.model_list.curselection()[0]
        self.model = self.models[selected_index]
