import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

labels = {0: 'Adult', 1: 'Business/Corporate', 2: 'Computers and Technology', 3: 'E-Commerce', 4: 'Education', 5: 'Food', 6: 'Forums', 7: 'Games', 8: 'Health and Fitness', 9: 'Law and Government', 10: 'News', 11: 'Photography', 12: 'Social Networking and Messaging', 13: 'Sports', 14: 'Streaming Services', 15: 'Travel'}

# Load the TfidfVectorizer that was used during training
with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

# Transform your input text using the loaded vectorizer
input_text = ["play football"]
input_text_transformed = tfidf_vectorizer.transform(input_text)

# Load the pre-trained model
with open("model2.pkl", "rb") as model_file:
    mf = pickle.load(model_file)

# Make predictions using the transformed text
predicted_labels = mf.predict(input_text_transformed)

# Map the predicted label to its corresponding category
predicted_category = labels.get(predicted_labels[0])

print(predicted_category)
