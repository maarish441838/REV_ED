from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# Load data and model
students = pd.read_csv('./data/student_data.csv')
materials = pd.read_csv('./data/learning_materials.csv')
model = joblib.load('./models/recommendation_model.pkl')

def prepare_single_student(student_data):
    # Create a DataFrame for the single student
    student_df = pd.DataFrame([student_data])

    # One-hot encode learning style and engagement
    features = pd.get_dummies(student_df, columns=['learning_style', 'engagement_level'])

    # Ensure all possible columns are present
    for col in [
        'learning_style_auditory', 'learning_style_kinesthetic', 'learning_style_visual',
        'engagement_level_high', 'engagement_level_low', 'engagement_level_medium'
    ]:
        if col not in features.columns:
            features[col] = 0

    # Normalize scores
    for subject in ['math', 'science', 'english']:
        features[f'{subject}_norm'] = features[f'{subject}_score'] / 100

    # Select relevant features in correct order
    feature_cols = [
        'math_norm', 'science_norm', 'english_norm',
        'learning_style_auditory', 'learning_style_kinesthetic', 'learning_style_visual',
        'engagement_level_high', 'engagement_level_low', 'engagement_level_medium'
    ]

    return features[feature_cols]

def recommend_materials(student_features, student_data):
    # Find similar students
    distances, indices = model.kneighbors(student_features)

    # Get similar students' data
    similar_students = students.iloc[indices[0]]

    # Recommend materials based on subjects where student needs improvement
    recommendations = []
    subjects = ['math', 'science', 'english']

    for subject in subjects:
        if student_data[f'{subject}_score'] < 70:  # If score is below 70, recommend materials
            subject_materials = materials[materials['subject'] == subject]

            # Filter by learning style
            style_materials = subject_materials[
                subject_materials['style'] == student_data['learning_style']
            ]

            # If no materials match learning style, take any
            if len(style_materials) == 0:
                style_materials = subject_materials

            # Sort by difficulty (start with easy)
            style_materials = style_materials.sort_values('difficulty')

            # Add top 2 materials per subject
            recommendations.extend(style_materials.head(2).to_dict('records'))

    return recommendations

def generate_quiz_questions(student_data):
    # Generate quiz questions based on student's level
    questions = []
    subjects = ['math', 'science', 'english']

    for subject in subjects:
        score = student_data[f'{subject}_score']
        if score < 50:
            difficulty = 'easy'
        elif score < 80:
            difficulty = 'medium'
        else:
            difficulty = 'hard'

        questions.append({
            'subject': subject,
            'difficulty': difficulty,
            'question': f"{subject.capitalize()} question ({difficulty})",
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correct_answer': 1  # Just for demo
        })

    return questions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        student_data = {
            'student_id': len(students) + 1,
            'math_score': float(request.form['math_score']),
            'science_score': float(request.form['science_score']),
            'english_score': float(request.form['english_score']),
            'learning_style': request.form['learning_style'],
            'engagement_level': request.form['engagement_level']
        }

        # Prepare features
        student_features = prepare_single_student(student_data)

        # Get recommendations
        recommendations = recommend_materials(student_features, student_data)

        # Generate quiz
        quiz_questions = generate_quiz_questions(student_data)

        return render_template('index.html',
                               recommendations=recommendations,
                               quiz_questions=quiz_questions,
                               student=student_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
