from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd
import os
import joblib
import numpy as np

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['student_database']
students_collection = db['students']

# Load the trained K-Means model
model_path = os.path.join("K-Means Clustering", "matching_algorithm.joblib")
kmeans_model = joblib.load(model_path)

# Subjects for matching criteria
score_columns = ['math', 'physics', 'english', 'history', 'geography', 'chemistry', 'biology']

@app.route('/add_student', methods=['POST'])
def add_student():
    student_data = request.json
    
    # Predict the student's cluster
    scores = [student_data['math'], student_data['physics'], student_data['english'],
              student_data['history'], student_data['geography'], student_data['chemistry'],
              student_data['biology']]
    cluster = kmeans_model.predict([scores])[0]
    
    # Add the cluster to the student data
    student_data['cluster'] = int(cluster)

    # Insert student data into the database
    students_collection.insert_one(student_data)
    return jsonify({"message": "Student added successfully!"})

@app.route('/get_students', methods=['GET'])
def get_students():
    students = list(students_collection.find({}, {"_id": 0}))
    return jsonify(students)

@app.route('/match_student', methods=['POST'])
def match_student():
    # Get student data from request
    student_data = request.json
    
    # Predict the student's cluster
    scores = [student_data['math'], student_data['physics'], student_data['english'],
              student_data['history'], student_data['geography'], student_data['chemistry'],
              student_data['biology']]
    cluster = kmeans_model.predict([scores])[0]
    
    # Fetch students in the same cluster from the database
    cluster_students = list(students_collection.find({"cluster": int(cluster)}, {"_id": 0}))
    print(f"Predicted cluster for student {student_data['student_id']}: {cluster}")  # Debugging purposes

    # Filter for students who have strengths in the student's "needs_help" subjects
    needs_help_subjects = student_data.get('needs_help', [])
    threshold = 70  # Define threshold for considering a subject as a strength
    matches = []
    
    for student in cluster_students:
        # Skip the student themselves
        if student['student_id'] == student_data['student_id']:
            continue
        
        # Check if this student has strengths in any of the "needs_help" subjects
        strengths = [subject for subject in score_columns if student.get(subject, 0) >= threshold]
        if any(subject in strengths for subject in needs_help_subjects):
            matches.append(student['student_id'])
    
    return jsonify({"matches": matches})

if __name__ == "__main__":      
    app.run(debug=True)
