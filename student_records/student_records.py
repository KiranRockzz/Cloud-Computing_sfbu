from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(_name_)

# MongoDB connection (we'll use environment variables later)
client = MongoClient('mongodb://localhost:27017/')
db = client['student_db']
scores = db['scores']

@app.route('/studentserver/api/score', methods=['GET'])
def get_score():
    student_id = request.args.get('student_id')
    score = scores.find_one({'student_id': student_id})
    if score:
        return jsonify({'student_id': score['student_id'], 'score': score['score']})
    return jsonify({'error': 'Student not found'}), 404

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)