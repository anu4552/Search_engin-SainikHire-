import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

function JobDetailPage() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/job/${id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) setError(data.error);
        else setJob(data);
      })
      .catch(() => setError("Failed to fetch job details"));
  }, [id]);

  if (error) {
    return (
      <div className="text-center mt-5">
        <h4 className="text-danger"> {error}</h4>
        <Link to="/search" className="btn btn-secondary mt-3">Back to Search</Link>
      </div>
    );
  }

  if (!job) return <p className="text-center mt-5"> Loading job details...</p>;

  return (
    <>
          <nav className="navbar navbar-expand-lg" style={{ backgroundColor: "#f0ecea" }}>
            <a className="navbar-brand" href="/">
              <img src="/img/logo.png" height="70px" width="140px" alt="Logo" style={{ borderRadius: "50%" }} />
            </a>
            <div className="collapse navbar-collapse">
              <ul className="navbar-nav mr-auto">
                <li className="nav-item"><a className="nav-link" href="/">Home</a></li>
                <li className="nav-item"><a className="nav-link" href="/searching">Search</a></li>
                <li className="nav-item"><a className="nav-link" href="/signuplogin">Recommendations</a></li>
                <li className="nav-item"><a className="nav-link" href="/sign">Register</a></li>
                <li className="nav-item"><a className="nav-link" href="#">CV Generator</a></li>
                <li className="nav-item"><a className="nav-link" href="#">Chatbot</a></li>
                <li className="nav-item"><a className="nav-link" href="/alljob">Latest Job Posts</a></li>
              </ul>
            </div>
          </nav>
    
<div
  className="container mt-5"
  style={{
    background: "rgb(250, 250, 250)",
    borderRadius: 16,
    boxShadow: "11px 4px 50px 19px rgb(151, 245, 252)",
    backdropFilter: "blur(6.4px)",
    WebkitBackdropFilter: "blur(6.4px)",
    border: "1px solid rgb(255, 255, 255)"
  }}
>
      <h1>{job.title}</h1><br/>
      <p><strong>Company:</strong>{job.company}</p>
      <p><strong>Location:</strong> {job.location}</p>
      <p><strong>Skills:</strong> {job.skills}</p>
      <p><strong>Education:</strong> {job.education}</p>
      <p><strong>Rank:</strong> {job.rank}</p>

      <p><strong>Date of posting job:</strong> {job.date_of_posting}</p>
      <p><strong>Last Date:</strong> {job.last_date}</p>
      <p><strong>Description:</strong></p>
      <p>{job.description}</p>
      <p>Apply link: <a href={job.apply_link} target="_blank">{job.apply_link}</a></p>
      <Link to="/searching" className="btn btn-outline-primary mt-3">Back to Search Page</Link>
    </div>
    </>
  );
}


export default JobDetailPage;
