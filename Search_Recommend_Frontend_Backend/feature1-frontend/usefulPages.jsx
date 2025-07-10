import React from 'react'
import {Link} from "react-router-dom";

const Pages = () => {
  const links = [
    { url: "https://www.exarmynaukri.com/", label: "Army Welfare Placement Organization" },
    { url: "https://www.ncs.gov.in/", label: "National Career Service" },
    { url:"https://dgrindia.gov.in/Content2/job-assistance/job-for-jcos-or", label:"Directorate General Resettlement"},
    { url: "https://upsc.gov.in/", label: "Union Public Service Commission" },
    { url: "https://ssc.nic.in/", label: "Staff Selection Commission" },
    { url:"https://www.indeed.com/q-Ex-Servicemen-jobs.html?vjk=dc65f98428ee7622", label:"Indeed"},

    { url: "https://www.skillindiadigital.gov.in/homehttps://www.nsdcindia.org/", label: "NSDC" },
    { url: "https://www.mygov.in/", label: "Government of India" },
    { url:"https://sparsh.defencepension.gov.in/", label:"Sparsh Principle Controller of Defence Account"},
  ];

  return (
    <>
      <div
      style={{
        minHeight:768,
        backgroundColor:"#c1dde8",
      }}>
      <div className="d-flex justify-content-center mt-3 "style={{borderRadius:"1px",borderColor:"White",
          backgroundColor:"#c1dde8"}}>
                <Link to="/alljob" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>All</Link>
                <Link to="/searching" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>Search</Link>
                <a href="#" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>ChatBot</a>
                  <Link to="/signupLogin" className="btn ms-2" style={{ borderRadius: "1px", borderColor: "white" }}>Job Recommendations</Link>
                  <a href="#" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>CV Generation</a>
                  <Link to="/jobupdate" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>Want to post job?</Link>
                  
                  <Link to="/pages" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>More Websites</Link>
                  
                </div>

 
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "36px",
        justifyContent: "center",
        backgroundColor:"#c1dde8",
      }}
    >
      <div style={{ width: "100%", textAlign: "center" }}>
        <h1><br/>Here are Some Important Websites</h1>
        <br />
      </div>
      {links.map((link, idx) => (
        <div
          key={idx}
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "20px 30px",
            background: "#f9f9f9",
            boxShadow: "0 2px 8px rgb(255, 255, 255)",
            minWidth: "220px",
            textAlign: "center"
          }}
        >
          <a
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: "#1976d2",
              textDecoration: "none",
              fontWeight: "bold",
              fontSize: "1.1rem"
            }}
          >
            {link.label}
          </a>
        </div>
      ))}
    </div>
    </div>
    </>
  );
}

export default Pages