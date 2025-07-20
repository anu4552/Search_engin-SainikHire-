import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Marquee from "react-fast-marquee";
import 'bootstrap/dist/css/bootstrap.min.css';

const jobs = [
  {
    title: "Laboratory assistant",
    apply: <a href="http://97.74.80.25:8081/2502/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Vacancy in Punjab for laboratory assistant, last date is 18th July, 2025",
  },
  {
    title: "Hindustan Aeronautic",
    apply: <a href="http://docs.lsadmin.site/uploads/lsdocs/Application_-_Annexure_-_I_1750662064.pdf" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Only one day left for Hindustan Aeronautic Limited; 7 Middle Specialist/Junior Specialist (Aircraft Division Nashik) required",
  },
  {
    title: "Tehri Hydro Development Corporation Limited",
    apply: <a href="https://recruitment.thdcil.in/FTB0625/Recruitment/Registration/NewApplicantRecruitment?JobAdv=QQBkAHYALQAwADYALwAyADAAMgA1AA%3D%3D&SubmitType=MgA%3D" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Tehri Hydro Development Corporation Limited (THDC) invites applications for 7 contractual posts of Field Engineer. Eligible candidates must apply online by 10-07-2025.",
  },
  {title: "CGHGCD Recruitment ",
    apply: <a href="https://etrpindia.com/Chh-fire/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "(Chhattisgarh Home Guard, Fire & SDRF). Eligible candidates must apply online by 31-07-2025.",
    
  },
  {title: "MECON Limited Executive Posts",
    apply: <a href="https://recruitment.meconlimited.co.in/Account/Login" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Roles for manager and deputy manager. Eligible candidates must apply online by 31-07-2025.",
  },
  {
    title: "SSC MTS & Havaldar",
    apply: <a href="https://ssc.gov.in/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Multi‑Tasking Staff & Havaldar, last date is 24th july,2025.",
  },


];

const jobs2 = [
  {
    title: " BPSC Bihar Special School Teacher",
    apply: <a href="https://www.bpsc.bihar.gov.in/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "7,279 vacancies – good for ex‑servicemen meeting eligibility.. Eligible candidates must apply online by 28-07-2025.",
  },
    {
    title: " ICFRE‑TFRI (Jabalpur)",
    apply: <a href="http://97.74.80.25:8081/2502/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Vacancy in Jabalpur for forest guard, driver, technical assistant, last date is 10th August, 2025",
  },
    {
    title: "Jobs via Directorate General Resettlement (DGR)",
    apply: <a href="  https://dgrindia.gov.in/content2/job-assistance/job-for-jcos-or" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Ongoing updates for ex-servicemen (JCOs/OR) in PSU, Govt & Private sectors. Eligible candidates must apply online by 20-07-2025.",
  },
    {
    title: " PFRDA Assistant Manager (Officer Grade A)",
    apply: <a href="https://www.pfrda.org.in/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Likely early–mid August 2025 (application period around June 23; typical duration 6–8 weeks, last date is 15th August, 2025",
  },

      {
    title: "SSC Selection Posts Phase‑XIII / 2025",
    apply: <a href="https://ssc.gov.in/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Multi-category Group ‘C’ roles including clerical and technical. Eligible candidates must apply online by 04-08-2025.",
  },
    {
    title: "RRB Technician Recruitment 2025",
    apply: <a href="http://97.74.80.25:8081/2502/" style={{color:"#ff0055", target:"_blank"}}>Apply Here</a>,
    body: "Posts of Technical Assistant, Forest Guard, Driver at ICFRE-TFRI, Jabalpur, last date is 10th August, 2025",
  },
];

function JobCard({ title, apply, body }) {
  return (
    <figure className="border rounded-xl p-4 m-2 bg-light shadow-sm" style={{ width: 250 }}>
      <div className="d-flex align-items-center gap-2 mb-2">
        <div>
          <figcaption className="fw-bold">{title}</figcaption>
          <small className="text-muted">{apply}</small>
        </div>
      </div>
      <blockquote className="mb-0">{body}</blockquote>
    </figure>
  );
}

function EntryPage() {
  const [input, setInput] = useState("");
  const [hover, setHover] = useState(false);
  const navigate = useNavigate();

  const search = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: input }),
      });
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      navigate("/searching", {
        state: { input, results: data },
      });
    } catch (error) {
      console.error("Search error:", error);
    }
  };

  return (
    <>
    <div className="d-flex justify-content-center mt-3 "style={{borderRadius:"1px",borderColor:"White",
    backgroundColor:"#F3F0EE"}}>
          <Link to="/alljob" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>All</Link>
          <Link to="/searching" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>Search</Link>
          <a href="#" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>ChatBot</a>
            <Link to="/signupLogin" className="btn ms-2" style={{ borderRadius: "1px", borderColor: "white" }}>Job Recommendations</Link>
            <a href="#" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>CV Generation</a>
            <Link to="/jobupdate" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>Want to post job?</Link>
            
            <Link to="/pages" className="btn ms-2" style={{ borderRadius: "0px", borderColor: "white" }}>More Websites</Link>
            
          </div>
      <div className="d-flex justify-content-center align-items-start" style={{ minHeight: '48vh', backgroundColor: '#F3F0EE', flexDirection: 'column', padding: '30px 0' }}>
      
        <form style={{ width: '500px', margin: '0 auto' }} onSubmit={search}>
          <div style={{ position: 'absolute', top: 20, left: 20 }}>
            <img src="/img/logo.png" height="60px" width="118px" style={{ borderRadius: "40%" }} alt="Logo" />
          </div>
          <div className="input-group shadow rounded-pill">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="form-control rounded-start-pill py-2 px-3"
              placeholder="Search Jobs with SainikHire"
            />
            <button
              type="submit"
              className="btn btn-primary rounded-end-pill px-4"
              onMouseEnter={() => setHover(true)}
              onMouseLeave={() => setHover(false)}
              style={{
                backgroundColor: hover ? '#f6cefc' : '#9269ec',
                borderColor: '#e7defa',
              }}
            >
              🔦
            </button>
          </div>
        </form>

        <div className="mt-5 w-100" style={{ backgroundColor: "#F3F0EE", padding: "10px 0" }}>
          <Marquee pauseOnHover speed={40} gradient={false}>
            {jobs.map((job) => (
              <JobCard
                key={job.apply}
                {...job}
                body={job.body.length > 70 ? job.body.slice(0, 70) + '...' : job.body}
              />
            ))}
          </Marquee>
        </div>
        <div className="mt-5 w-100" style={{ backgroundColor: "#F3F0EE", padding: "10px 0" }}>
          <Marquee pauseOnHover speed={40} gradient={false}>
            {jobs2.map((job) => (
              <JobCard
                key={job.apply}
                {...job}
                body={job.body.length > 70 ? job.body.slice(0, 70) + '...' : job.body}
              />
            ))}
          </Marquee>
        </div>
      </div>
    </>
  );
}

export default EntryPage;
