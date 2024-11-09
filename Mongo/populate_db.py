from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://mongo:27017/")  # Update for Docker or local setup
db = client['student_db']
collection = db['students']

df = pd.read_csv('student_data.csv')

collection.insert_many(df.to_dict('records'))
print("Sample data added successfully.")
