import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

df = pd.read_csv("spam.csv", encoding="latin-1")

df = df[['v1', 'v2']]
df.columns = ['label', 'message']

df['label'] = df['label'].map({'ham': 0, 'spam': 1})

tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df['message'])

y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# 👇 ADD THESE LINES HERE AT THE BOTTOM
message = ["Congratulations! You won ₹50,000. Click here now!"]

message_vector = tfidf.transform(message)

prediction = model.predict(message_vector)

if prediction[0] == 1:
    print("Spam 🚫")
else:
    print("Ham ✅")

    import pickle

# Save the trained model
pickle.dump(model, open('spam_model.pkl', 'wb'))

# Save the TF-IDF vectorizer
pickle.dump(tfidf, open('vectorizer.pkl', 'wb'))

print("Model and vectorizer saved successfully!")