#task 2 - lab 09

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#sample dataset
example_data = {
    'message_body': [
        'limited time discount click now',
        'team meeting tomorrow at 10am',
        'claim your free gift today',
        'report draft attached',
        'you have been selected winner',
        'project deadline next Monday',
        'unlock exclusive access now',
        'lunch with the marketing team',
        'special offer just for you',
        'weekly summary attached'
    ],
    'is_spam': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1=spam, 0=not spam
}

df = pd.DataFrame(example_data)

#TF-IDF feature extraction
tfidf = TfidfVectorizer(max_features=1000)
features = tfidf.fit_transform(df['message_body'])

#labels
labels = df['is_spam']

#train/test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

#train an SVM classifier
spam_classifier = SVC(kernel='linear', probability=True, random_state=42)
spam_classifier.fit(X_train, y_train)

#predict on test set
y_pred = spam_classifier.predict(X_test)

#evaluate performance
acc = accuracy_score(y_test, y_pred)
print(f"model accuracy: {acc:.2f}\n")

print("detailed classification report:")
print(classification_report(y_test, y_pred))

conf_mat = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues')
plt.xlabel('predicted label')
plt.ylabel('true label')
plt.title('spam classifier confusion matrix')
plt.show()

#classify a new message
new_message = ["don’t miss out on this exclusive opportunity"]
new_vec = tfidf.transform(new_message)
new_pred = spam_classifier.predict(new_vec)[0]
print(f"\nnew message is classified as: {'Spam' if new_pred == 1 else 'Not Spam'}")
