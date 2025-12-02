import pickle
from sklearn.preprocessing import LabelEncoder

# 🚨 Make sure to replace these with actual classes used during model training
labels = ['speech', 'noise', 'scream']  # Example class list used for encoding

le = LabelEncoder()
le.fit(labels)

# Save the encoder to file
with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

print("✅ label_encoder.pkl generated successfully.")
