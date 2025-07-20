import React, { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";

function Recommendation() {
  const location = useLocation();
  const user_email = location.state?.user_email || "";
  const [results, setResults] = useState(location.state?.jobs || []);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchRecommendations = async () => {
      if (!user_email) return;
      setLoading(true);
      try {
        const response = await fetch("http://127.0.0.1:5000/recommend", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_input: user_email }),
        });
        const data = await response.json();
        setResults(data);
      } catch (err) {
        console.error("Recommendation fetch failed:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [user_email]);

  return (
    <div style={{ minHeight: '100vh', width: '100vw', background: '#F3F0EE', paddingTop: '50px', paddingLeft:'20px', fontFamily: 'Segoe UI, sans-serif' }}>
      <center>
        <section style={{ maxWidth: 900, background: 'rgb(255, 228, 246)', borderRadius: 14, padding: '22px 20px 12px' }}>
          <h3 style={{ color: 'rgb(124, 0, 89)', fontWeight: 700, marginBottom: 20 }}>
            Job Recommendations by SainikHire<br/>
          </h3>
          <h6>For the user {user_email}</h6>

          {loading && (
            <div style={{ textAlign: 'center', marginTop: 24 }}>
              <p style={{ color: '#5e35b1', fontWeight: 500 }}>Fetching suitable jobs...</p>
            </div>
          )}

          {!loading && results.length > 0 && (
            <div style={{ marginTop: 24 }}>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 17 }}>
                {results.map((job, index) => (
                  <Link
                    key={index}
                    to={`/job/${job._id}`}
                    style={{
                      textDecoration: 'none',
                      borderRadius: 10,
                      border: '2px solid rgb(246, 246, 246)',
                      boxShadow: '0 1px 4px rgb(255, 254, 254)',
                      maxWidth: 300,
                      flex: '1 1 220px',
                      padding: '16px 14px',
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 600, color: 'rgb(160, 2, 115)', marginBottom: 6, fontSize:20, backgroundColor:'rgb(254, 215, 243)' }}>
                        {job.title}
                      </div>
                      <div style={{ color: '#444000', fontSize: 15 }}>
                        {job.description?.slice(0, 140)}...
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {!loading && results.length === 0 && (
            <div style={{ textAlign: 'center', marginTop: 24 }}>
              <p style={{ color: '#d32f2f', fontWeight: 500 }}>No recommendations found for your email.</p>
            </div>
          )}
        </section>
      </center>
    </div>
  );
}

export default Recommendation;
