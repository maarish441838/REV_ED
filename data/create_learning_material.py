import pandas as pd

materials = {
    'material_id': range(1, 21),
    'subject': ['math']*7 + ['science']*7 + ['english']*6,
    'difficulty': ['easy', 'medium', 'hard']*6 + ['easy', 'medium'],
    'style': ['visual', 'auditory', 'kinesthetic']*6 + ['visual', 'auditory'],
    'title': [
        'Math Basics Video', 'Algebra Podcast', 'Math Hands-on Activity',
        'Geometry Visual Guide', 'Calculus Audio Lesson', 'Math Puzzle Game',
        'Advanced Math Concepts',
        'Science Fundamentals Video', 'Chemistry Podcast', 'Biology Lab Simulation',
        'Physics Visual Guide', 'Earth Science Audio', 'Science Experiment Guide',
        'Advanced Science Concepts',
        'Grammar Video Course', 'Literature Podcast', 'Writing Workshop',
        'Reading Comprehension Guide', 'Vocabulary Audio Lessons', 'Creative Writing Exercises'
    ],
    'url': [
        'https://example.com/math1', 'https://example.com/math2', 'https://example.com/math3',
        'https://example.com/math4', 'https://example.com/math5', 'https://example.com/math6',
        'https://example.com/math7',
        'https://example.com/science1', 'https://example.com/science2', 'https://example.com/science3',
        'https://example.com/science4', 'https://example.com/science5', 'https://example.com/science6',
        'https://example.com/science7',
        'https://example.com/english1', 'https://example.com/english2', 'https://example.com/english3',
        'https://example.com/english4', 'https://example.com/english5', 'https://example.com/english6'
    ]
}

materials_df = pd.DataFrame(materials)
materials_df.to_csv('data/learning_materials.csv', index=False)