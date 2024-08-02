from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
import socket

app = Flask(_name_)
app.config["MONGO_URI"] = "mongodb://" + os.getenv("MONGO_URL") + "/" + os.getenv("MONGO_DATABASE")
mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(message="Welcome to bookshelf app! I am running inside {} pod!".format(hostname))

@app.route("/books")
def get_all_tasks():
    books = db.bookshelf.find()
    data = [{"id": str(book["_id"]), "Book Name": book["book_name"], "Book Author": book["book_author"], "ISBN": book["ISBN"]} for book in books]
    return jsonify(data)

@app.route("/book", methods=["POST"])
def add_book():
    book = request.get_json(force=True)
    db.bookshelf.insert_one({"book_name": book["book_name"], "book_author": book["book_author"], "ISBN": book["isbn"]})
    return jsonify(message="Task saved successfully!")

@app.route("/book/<id>", methods=["PUT"])
def update_book(id):
    data = request.get_json(force=True)
    response = db.bookshelf.update_one({"_id": ObjectId(id)}, {"$set": {"book_name": data['book_name'], "book_author": data["book_author"], "ISBN": data["isbn"]}})
    message = "Task updated successfully!" if response.matched_count else "No book found!"
    return jsonify(message=message)

@app.route("/book/<id>", methods=["DELETE"])
def delete_task(id):
    response = db.bookshelf.delete_one({"_id": ObjectId(id)})
    message = "Task deleted successfully!" if response.deleted_count else "No book found!"
    return jsonify(message=message)

@app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    db.bookshelf.delete_many({})
    return jsonify(message="All Books deleted!")

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)
