import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load your dataset (replace 'your_data.csv' with your CSV file)
df = pd.read_csv('categories.csv')

# Preprocessing: Combine domain and title into a single text_data column
df['text_data'] = df['title'] + ' ' + df['domain']

# Label Encoding
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['category'])

# Feature Extraction using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # Limit the number of features for faster training
X = tfidf_vectorizer.fit_transform(df['text_data'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, df['label'], test_size=0.2, random_state=42)

# Choose a classification model (e.g., Multinomial Naive Bayes)
# model = MultinomialNB(alpha=0.1)  # Fine-tune the alpha hyperparameter
# model = DecisionTreeClassifier()
# model = RandomForestClassifier(n_estimators=100, random_state=42) #0.75 exact but not giving acurate results
# from sklearn.svm import SVC
# model = SVC(kernel='linear', C=1.0) # 0.607
from sklearn.linear_model import LogisticRegression
# model = LogisticRegression(max_iter=1000)
from sklearn.neural_network import MLPClassifier
model = MLPClassifier(hidden_layer_sizes=(100,100), max_iter=1000)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print a classification report for more metrics
# print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save the trained model
joblib.dump(model, 'website_classifier_model.joblib')
print("Successfully trained model")
