import pandas as pd
import random

# Number of additional students to generate
num_additional_students = 60

# List of subjects and availability times
subjects = ['math', 'physics', 'english', 'history', 'geography', 'chemistry', 'biology']
availability = [
    'Monday 10 AM - 12 PM', 'Monday 2 PM - 4 PM',
    'Tuesday 10 AM - 12 PM', 'Tuesday 2 PM - 4 PM',
    'Wednesday 10 AM - 12 PM', 'Wednesday 2 PM - 4 PM'
]

# Load existing data if it exists, otherwise create an empty DataFrame
try:
    df = pd.read_csv('student_data.csv')
    start_id = df['student_id'].str.extract('(\d+)').astype(int).max().values[0] + 1  # Continue IDs from the last existing ID
except FileNotFoundError:
    df = pd.DataFrame()
    start_id = 1  # Start IDs from 1 if file doesn't exist

# Generate additional synthetic data
data = []
for i in range(start_id, start_id + num_additional_students):
    student = {
        "student_id": f"S{i}",
        "math": random.randint(50, 100),
        "physics": random.randint(50, 100),
        "english": random.randint(50, 100),
        "history": random.randint(50, 100),
        "geography": random.randint(50, 100),
        "chemistry": random.randint(50, 100),
        "biology": random.randint(50, 100),
        "needs_help": random.sample(subjects, k=random.randint(1, 2)),  # Subjects needing help
        "availability": random.sample(availability, k=2)  # Randomly assign 2 time slots
    }
    data.append(student)

# Convert the additional data to DataFrame
new_df = pd.DataFrame(data)

# Append the new data to the existing DataFrame
df = pd.concat([df, new_df], ignore_index=True)

# Save the updated DataFrame to the CSV file
df.to_csv('student_data.csv', index=False)
print('Data saved successfully')
