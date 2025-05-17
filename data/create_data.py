import pandas as pd
import numpy as np

# Create simulated student data
np.random.seed(42)
num_students = 100

data = {
    'student_id': range(1, num_students+1),
    'math_score': np.random.normal(70, 15, num_students).clip(0, 100),
    'science_score': np.random.normal(65, 12, num_students).clip(0, 100),
    'english_score': np.random.normal(75, 10, num_students).clip(0, 100),
    'learning_style': np.random.choice(['visual', 'auditory', 'kinesthetic'], num_students),
    'engagement_level': np.random.choice(['low', 'medium', 'high'], num_students, p=[0.2, 0.5, 0.3])
}

df = pd.DataFrame(data)
df.to_csv('data/student_data.csv', index=False)