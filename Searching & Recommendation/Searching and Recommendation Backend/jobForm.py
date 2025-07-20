from flask import Flask, request, jsonify

def jobupdate(model, collection):
    data = request.json

    data['skills_embedding'] = model.encode(data['skills']).tolist()

    educations = data.get('education', '')
    location = data.get('location')
    rank=data.get('rank')
    combined_text = f"{educations} {data['skills']} {location} {rank}"
    data['all_combined_embedding'] = model.encode(combined_text).tolist()

    required_fields = ['title','company','description', 'skills','location', 'rank','education','date_of_posting','last_date','apply_link' ]
    
    errors = {field: "This field is required" for field in required_fields if not data.get(field)}
    
    if errors:
        return jsonify({"errors": errors}), 400

    collection.insert_one(data)
    return jsonify({"message": "Signed In"}), 200
