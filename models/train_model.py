import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib

# Load student data and learning materials
students = pd.read_csv('./data/student_data.csv')
materials = pd.read_csv('./data/learning_materials.csv')

# Feature engineering
def prepare_features(students):
    # One-hot encode learning style and engagement
    features = pd.get_dummies(students, columns=['learning_style', 'engagement_level'])
    
    # Normalize scores
    for subject in ['math', 'science', 'english']:
        features[f'{subject}_norm'] = features[f'{subject}_score'] / 100
    
    # Select relevant features for recommendation
    feature_cols = [
        'math_norm', 'science_norm', 'english_norm',
        'learning_style_auditory', 'learning_style_kinesthetic', 'learning_style_visual',
        'engagement_level_high', 'engagement_level_low', 'engagement_level_medium'
    ]
    
    return features[feature_cols]

# Prepare features
student_features = prepare_features(students)

# Train KNN model for recommendations
model = NearestNeighbors(n_neighbors=5, metric='cosine')
model.fit(student_features)

# Save the model
joblib.dump(model, 'models/recommendation_model.pkl')

print("Model trained and saved successfully!")