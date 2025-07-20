import React, { useState} from "react";
import { useLocation, Link } from "react-router-dom";
import {useEffect} from "react";
import Marquee from "react-fast-marquee";

function SearchPage() {
  const location = useLocation();
  const initialInput = location.state?.input || "";
  const initialResults = location.state?.results || [];

  const [input, setInput] = useState(initialInput);
  const [results, setResults] = useState(initialResults);
  const [loading, setLoading] = useState(false);
  const [hover, setHover] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    const response = await fetch("http://127.0.0.1:5000/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: input }),
    });

    const data = await response.json();
    setResults(data);
    setLoading(false);
    //e.stopPropagation();
  };

  useEffect(() => {
    sessionStorage.setItem("searchInput", input);
    sessionStorage.setItem("searchResults", JSON.stringify(results));
  }, [input, results]);


  return (
    <div style={{ minHeight: '100vh', width: '100vw', backgroundColor: '#F3F0EE', paddingTop: '50px', position: 'relative' }}>
      <div style={{ position: 'absolute', top: 20, left: 20 }}>
        <img src="/img/logo2.png" height="60px" width="118px" style={{ borderRadius: "5%" }} alt="Logo" />
      </div>

      <form
        onSubmit={handleSearch}
        className="d-flex flex-column align-items-center"
        style={{ maxWidth: '600px', margin: '0 auto' }}
      >
        <div className="input-group shadow rounded-pill w-100 align-items-center">
          <input
            type="text"
            className="form-control rounded-start-pill py-2 px-3"
            placeholder="Write your skills and education"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            type="submit"
            className="btn btn-primary rounded-end-pill px-4"
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
            style={{
              backgroundColor: hover ? '#f9f050' : '#9269ec',
              borderColor: '#e7defa',
            }}
          >
            🔦
          </button>
        </div>
      </form>
      <Marquee
        style={{ backgroundColor: "#ffffcc" }}
        pauseOnHover={true}
        pauseOnClick={false}
      >
        <span style={{ marginRight: "2rem"}}>Vacancy in Punjab for laboratory assistant, last date is 18th July, 2025; <a href="http://97.74.80.25:8081/2502/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a></span>
        <span style={{ marginRight: "2rem"}}>Only one day left for Hindustan Aeronautic Limited; 7 Middle Specialist/Junior Specialist (Aircraft Division Nashik) required <a href="http://docs.lsadmin.site/uploads/lsdocs/Application_-_Annexure_-_I_1750662064.pdf" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a></span>
        <span style={{ marginRight: "2rem" }}>Tehri Hydro Development Corporation Limited (THDC) invites applications for 7 contractual posts of Field Engineer. Eligible candidates must apply online by 10-07-2025.
        <a href="https://recruitment.thdcil.in/FTB0625/Recruitment/Registration/NewApplicantRecruitment?JobAdv=QQBkAHYALQAwADYALwAyADAAMgA1AA%3D%3D&SubmitType=MgA%3D" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>
        </span>
      </Marquee>
      <div className="d-flex justify-content-center mt-3 "style={{borderRadius:"1px",borderColor:"White"}}>
      <Link to="/alljob" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>All</Link>
      <a href="#" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>ChatBot</a>
        <Link to="/signupLogin" className="btn ms-2" style={{ borderRadius: "1px", borderColor: "white" }}>Job Recommendations</Link>
        <a href="#" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>CV Generation</a>
        <Link to="/jobupdate" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>Want to post job?</Link>
        
        <Link to="/pages" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>More Websites</Link>
        
      </div>

      {loading && (
        <div className="text-center mt-4">
          <p>Searching jobs...</p>
        </div>
      )}
      {!loading && results.length > 0 && (
        <div className="container mt-5">
          {results.map((job, index) => (
            <div key={index} className="card p-3 my-3"
            style={{ backgroundColor: '#F5F5F5', borderRadius: '0px', borderColor: '#e7defa' }}>
              <h5>
                <Link to={`/job/${job._id}`} style={{ textDecoration: 'none', color: '#5e35b1' }}>
                  {job.title}
                </Link>
             
              {job.verified === "true" && (<span style={{
              marginLeft: "10px",
              color: "green",
              fontSize: "14px",
              fontWeight: "bold",
              border: "1px solid green",
              borderRadius: "4px",
              padding: "2px 6px",
              backgroundColor: "#e8f5e9"
            }}>
              Verified
            </span>)}
            </h5>
              <p>{job.description?.slice(0, 550)}...</p>
            </div>
          ))}
        </div>
      )}

      {!loading && results.length === 0 && input !== "" && (
        <div className="text-center mt-4">
          <p className="text-danger">Job not detected</p>
        </div>
      )}
    </div>
  );
}

export default SearchPage;
