from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd 
# Create a LabelEncoder
label_encoder = LabelEncoder()

# Fit the encoder on your original labels
df = pd.read_csv('categories.csv')
category = df["title"]
# print(category,"category")
# original_labels = ['label1', 'label2', 'label3']
encoder = label_encoder.fit_transform(category)

# Save the label encoder to a file
joblib.dump(label_encoder, 'label_encoder.joblib')
