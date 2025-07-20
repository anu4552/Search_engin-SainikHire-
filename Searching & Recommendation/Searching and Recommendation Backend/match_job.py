import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# searching logic
def match_job(user_input, model, collection, top_k=20):
    try:
        user_emb = model.encode(user_input).reshape(1, -1)
    except Exception as e:
        return []

    results = []
    for job in collection.find({"all_combined_embedding": {"$exists": True}}):
        try:
            job_emb = np.array(job["all_combined_embedding"]).reshape(1, -1)
            score = cosine_similarity(user_emb, job_emb)[0][0]
            job["score"] = round(float(score), 4)
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
        except:
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
