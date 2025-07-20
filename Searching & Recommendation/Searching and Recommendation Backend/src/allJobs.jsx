import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';

function AllJobs() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null);

  const [currentPage, setCurrentPage] = useState(1);
  const jobsPerPage = 15;

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/alljobs");
        if (!response.ok) {
          throw new Error("Can't fetch jobs");
        }
        const data = await response.json();
        setResults(data);
      } catch (error) {
        console.error("Error:", error);
        setError("Error in fetching jobs!");
      } finally {
        setLoading(false);
      }
    };
    fetchJobs();
  }, []);

  const indexOfLastJob = currentPage * jobsPerPage;
  const indexOfFirstJob = indexOfLastJob - jobsPerPage;
  const currentJobs = results.slice(indexOfFirstJob, indexOfLastJob);
  const totalPages = Math.ceil(results.length / jobsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

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
            <li className="nav-item"><a className="nav-link" href="/signupLogin">Recommendations</a></li>
            <li className="nav-item"><a className="nav-link" href="#">CV Generator</a></li>
            <li className="nav-item"><a className="nav-link" href="#">Chatbot</a></li>
            <li className="nav-item"><a className="nav-link" href="#">Latest Job Posts</a></li>
          </ul>
        </div>
      </nav>

      <div style={{ minHeight: '100vh', width: '100vw', backgroundColor: '#F3F0EE', paddingTop: '50px' }}>
        {loading && <div className="text-center mt-5">Loading!</div>}
        {error && <div className="text-center mt-5 text-danger">{error}</div>}

        {!loading && results.length > 0 && (
          <div className="container mt-5">
            {currentJobs.map((job) => (
              <div key={job._id} className="mb-4 p-3 border rounded bg-white">
                <a href={`/job/${job._id}`} style={{ textDecoration: 'none', color: '#5e35b1' }}>
                  <h5>{job.title}</h5>
                </a>
                <p>{job.description?.slice(0, 500) || job.body?.slice(0, 500) || "No description"}...</p>
              </div>
            ))}

            <nav className="d-flex justify-content-center mt-4">
              <ul className="pagination">
                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                  <button className="page-link" onClick={() => handlePageChange(currentPage - 1)}>Previous</button>
                </li>

                {[...Array(totalPages).keys()].map((num) => (
                  <li key={num} className={`page-item ${currentPage === num + 1 ? 'active' : ''}`}>
                    <button className="page-link" onClick={() => handlePageChange(num + 1)}>
                      {num + 1}
                    </button>
                  </li>
                ))}

                <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                  <button className="page-link" onClick={() => handlePageChange(currentPage + 1)}>Next</button>
                </li>
              </ul>
            </nav>
          </div>
        )}

        {!loading && results.length === 0 && !error && (
          <div className="text-center mt-5">No jobs found.</div>
        )}
      </div>
    </>
  );
}

export default AllJobs;
