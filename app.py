from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, get_flashed_messages
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import json

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.secret_key = SECRET_KEY

MONGO_URI = os.getenv('MONGO_URL')
# Create a new client and connect to the server
client = MongoClient(MONGO_URI)
db = client.test

collection = db["users"]

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/users', methods=["POST"])
def add():
    try:
        data = request.form.to_dict()
        collection.insert_one(data)
        flash('Data submitted successfully')
        return redirect(url_for('users'))
    except Exception as e:
        print(f"Error: {e}")  # optional: helpful for debugging
        return jsonify({
            "message": "Error while saving data",
            "status":False,
            "data" : []
        }), 500
    
@app.route('/users',methods=["GET"])
def users():
    data = list(collection.find())
    result = [{**doc, '_id': str(doc['_id'])} for doc in data]
    return render_template('users.html', result=result)

@app.route('/api', methods=["GET"])
def get_data():
    with open("data.json",mode="r", encoding="UTF+8") as file:
       data = json.load(file)
    return jsonify({
            "status":True,
            "data" : data
        }), 200

@app.route('/submittodoitem', methods=["POST"])
def add():
    try:
        to_do_collection = db["to_do"]
        data = request.form.to_dict()
        to_do_collection.insert_one(data)
        flash('Data submitted successfully')
        return redirect(url_for('users'))
    except Exception as e:
        print(f"Error: {e}")  # optional: helpful for debugging
        return jsonify({
            "message": "Error while saving data",
            "status":False,
            "data" : []
        }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000")