## Desktop Organizer with AI
This is a script that uses machine learning to automatically organize your desktop. It classifies your files based on their contents and moves them into subdirectories for each label. This project uses tkinter for the user interface, nltk and sklearn for the machine learning part, and python-magic to determine file types.

# Features
* Train a new model on your own data.
* Classify and organize your desktop files using a trained model.
* Load a pre-trained model.
* Select from multiple trained models.
* Backup and restore your desktop.

# Installation
1. Clone this repository to your local machine.
2. Install the necessary Python libraries. You can do this by running the following command: ``` pip install -r requirements.txt ```

# Usage
``` python main.py ```

When you run the script, a GUI will open. Here are the functions of each button:

* "Train a New Model": Asks for a directory with subdirectories. Each subdirectory should contain text files of a single category. For example, if you provide a directory with two subdirectories "Invoices" and "Reports", each containing appropriate files, it will train a model to classify files into these categories.

* "Organize Desktop": Uses the selected model to classify each file on your desktop and moves it into a subdirectory for its predicted label.

* "Load a Model": Allows you to load a pre-trained model from a file.

* "Select a Model": Lets you select a model from the list of trained models.

* "Backup Desktop": Makes a backup of your current desktop.

* "Restore Desktop": Restores your desktop from the last backup.
