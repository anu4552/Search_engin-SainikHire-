from flask import Flask, request, jsonify

def signup(collection):
    data = request.json
    required_fields = ['name', 'email', 'password', 'education', 'skills', 'rank', 'location']
    errors = {field: "fill all fields" for field in required_fields if not data.get(field)}
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    if collection.find_one({'email': data['email']}):
        return jsonify({"errors": {"email": "Email already exists"}})
    if collection.find_one({'password': data['password']}):
        return jsonify({"errors": {"password": "Enter another password"}})

    collection.insert_one(data)
    return jsonify({"message": "Signed In"}), 200