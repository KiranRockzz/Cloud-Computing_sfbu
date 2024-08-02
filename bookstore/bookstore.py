from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(_name_)

# MongoDB connection (we'll use environment variables later)
client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore_db']
books = db['books']

@app.route('/bookshelf/books', methods=['GET'])
def get_books():
    return jsonify([book for book in books.find()])

@app.route('/bookshelf/book', methods=['POST'])
def add_book():
    book = request.json
    result = books.insert_one(book)
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/bookshelf/book/<id>', methods=['PUT'])
def update_book(id):
    books.update_one({'_id': ObjectId(id)}, {'$set': request.json})
    return jsonify({'result': 'success'})

@app.route('/bookshelf/book/<id>', methods=['DELETE'])
def delete_book(id):
    books.delete_one({'_id': ObjectId(id)})
    return jsonify({'result': 'success'})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
