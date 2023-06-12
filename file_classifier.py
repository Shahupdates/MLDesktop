import os
from pathlib import Path
import shutil
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import magic
from datetime import datetime
import joblib

class FileClassifier:
    def __init__(self):
        self.model = None

    def classify_files(self):
        """Classify text files on the desktop using the loaded model."""
        if not self.model:
            messagebox.showinfo("Error", "No model loaded!")
            return

        path = Path.home() / "Desktop"
        files = path.iterdir()
        mime = magic.Magic(mime=True)
        
        for file in files:
            if file.is_dir():
                continue
            
            mimetype = mime.from_file(str(file))
            if "text" in mimetype:
                try:
                    with open(file, 'r') as f:
                        text = f.read()
                        features = self.model.vectorizer.transform([text])
                        label = self.model.predict(features)[0]
                except Exception as e:
                    messagebox.showinfo("Error", f"Could not open file {file}. Error: {e}")
                    continue
                
                date = datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d')
                new_dir = path / label / date
                new_dir.mkdir(parents=True, exist_ok=True)
                
                shutil.move(str(file), str(new_dir))

    def load_model(self):
        """Load a model from a file selected by the user."""
        file_path = Path(filedialog.askopenfilename())
        if not file_path.is_file():
            return
        try:
            self.model = joblib.load(str(file_path))
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to load the model! Error: {e}")

    def select_model(self, models):
        """Select a model from the list of loaded models.
        
        Args:
            models (list): A list of loaded models.
        """
        if not models:
            messagebox.showinfo("Error", "No models available!")
            return

        selected_index = self.model_list.curselection()
        if not selected_index:
            messagebox.showinfo("Error", "No model selected!")
            return

        self.model = models[selected_index[0]]
