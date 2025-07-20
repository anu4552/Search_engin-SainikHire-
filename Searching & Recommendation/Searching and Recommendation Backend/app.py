from flask import Flask, request, jsonify
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import numpy as np
from bson import ObjectId
from match_job import match_job
from recommend_job_logic import recommend_jobs_logic
from signupForm import signup
from jobForm import jobupdate
from data_deletion import delete_expired_jobs
from email_sending import send_job_reminders
from updating_database import updateJobs
from updating_from_dgr import extracted_jobs

app = Flask(__name__)
CORS(app) 

client = MongoClient("mongodb://localhost:27017/")
db = client["SainikHire"]
collection = db["database1"]

model = SentenceTransformer("all-MiniLM-L6-v2")

collection2 = db['users']

# signup page
@app.route('/signup', methods=['POST'])
def signup():
    User_Signup = signup(collection2)
    return User_Signup


# routing recommendation logic
@app.route("/recommend", methods=["POST"])
def recommend_jobs():
    data = request.get_json()
    user_input = data.get("user_input", "")
    if not user_input:
        return jsonify([])

    results = recommend_jobs_logic(user_input, db, model, collection)
    return jsonify(results)


# searching route
@app.route("/search", methods=["POST"])
def search_match():
    data = request.get_json()
    user_input = data.get("user_input", "")
    matches = match_job(user_input, model, collection)
    return jsonify(matches)


# job post routing
@app.route("/job/<id>", methods=["GET"])
def get_job(id):
    job = collection.find_one({"_id": ObjectId(id)})
    if not job:
        return jsonify({"error": "Job not found"}), 404
    job["_id"] = str(job["_id"]) 
    return jsonify(job)


# routing jobupdates
@app.route('/jobupdate', methods=['POST'])
def jobupdates():
    form = jobupdate(model, collection)
    return form


# all jobs are displayed
@app.route("/alljobs", methods=["GET"])
def allJob():
    data = list(collection.find())
    for job in data:
        job["_id"] = str(job["_id"]) 
    return jsonify(data)

#deleting cross last date data
delete_expired_jobs();

# sending remainder
send_job_reminders();

#updating database every hour, through web scrapping from ncs portal
updateJobs()

#updating database in one day from dgr website
extracted_jobs()

if __name__ == "__main__":
    app.run(debug=True)
