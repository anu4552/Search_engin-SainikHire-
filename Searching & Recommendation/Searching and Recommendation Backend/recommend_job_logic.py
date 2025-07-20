import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# recommendation logic
def recommend_jobs_logic(user_input,db, model, collection, top_k=6):
    if '@gmail.com' in user_input:
        user = db['users'].find_one({'email': user_input})
    else:
        user = db['users'].find_one({'password': user_input})
    try:
        if not user or 'skills' not in user:
            return []
        user_skill = ' '.join(user['skills'])
        user_emb = model.encode(user_skill).reshape(1, -1)
    except Exception as e:
        return []

    results = []
    for job in collection.find({"skills_embedding": {"$exists": True}}):
        try:
            job_emb = np.array(job["skills_embedding"]).reshape(1, -1)
            score = cosine_similarity(user_emb, job_emb)[0][0]
            results.append({
                "_id": str(job["_id"]),
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "date_of_posting": job.get("date_of_posting", ""),
                "last_date": job.get("last_date", ""),
                "rank": job.get("rank", ""),
                "education": job.get("education", ""),
                "location": job.get("location", ""),
                "description": job.get("description", ""),
                "skills": job.get("skills", ""),
                "apply_link": job.get("apply_link", ""),
                "score": round(float(score), 4)
            })
        except Exception as e:
            print("Skip job due to error:", e)
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
