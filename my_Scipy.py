import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the serialized model from the "model2.pkl" file
with open("model2.pkl", "rb") as f:
    loaded_model = pickle.load(f)

# Define the labels mapping (customize this based on your actual labels)
labels = {0: 'Dumb', 1: 'Smart', 2: 'Oversmart'}

# Input text for classification
input_text = ["My name is Deepak"]  # Note the input as a list

# Create and fit the TF-IDF vectorizer on your training data
tfidf_vectorizer = TfidfVectorizer()
training_data = ["I am Oversmart idiot"]  # Replace with your actual training data
tfidf_vectorizer.fit(training_data)

# Use the fitted vectorizer to transform the input text
X_input = tfidf_vectorizer.transform(input_text)

# Use the loaded model to make predictions
predicted_class_indices = loaded_model.predict(X_input)
print(predicted_class_indices)
# Map predicted class index to label
predicted_label = labels.get(predicted_class_indices[0])

# Print the predicted label
print("Predicted category:", predicted_label)
