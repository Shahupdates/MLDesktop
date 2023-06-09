import os
import shutil
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

nltk.download('stopwords')

# Get the list of stopwords
stopwords = set(stopwords.words('english'))

# This is the path to the directories with your training files
work_dir = os.path.expanduser("~/Desktop/Work")
personal_dir = os.path.expanduser("~/Desktop/Personal")

# Get the list of all files in each directory
work_files = os.listdir(work_dir)
personal_files = os.listdir(personal_dir)

# Create lists to store the file contents and their labels
texts = []
labels = []

# Load the work files
for file in work_files:
    with open(os.path.join(work_dir, file), 'r') as f:
        texts.append(f.read())
        labels.append('Work')

# Load the personal files
for file in personal_files:
    with open(os.path.join(personal_dir, file), 'r') as f:
        texts.append(f.read())
        labels.append('Personal')

# Create the CountVectorizer
vectorizer = CountVectorizer(stop_words=stopwords)

# Convert the texts into feature vectors
X = vectorizer.fit_transform(texts)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train the model
model = MultinomialNB().fit(X_train, y_train)

# Test the model
print("Model Accuracy: ", model.score(X_test, y_test))

# Now you can use the model to organize other text files on your desktop
path = os.path.expanduser("~/Desktop")
files = os.listdir(path)

for file in files:
    with open(os.path.join(path, file), 'r') as f:
        text = f.read()
        features = vectorizer.transform([text])
        label = model.predict(features)
        
        # Create the directory if it doesn't already exist
        new_dir = os.path.join(path, label[0])
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        
        # Move the file
        shutil.move(os.path.join(path, file), new_dir)
