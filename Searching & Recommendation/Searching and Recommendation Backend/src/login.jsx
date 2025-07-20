import React from 'react'

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';


function Login() {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState();
  const navigate = useNavigate();

  const handleLogin = (e) => {
  e.preventDefault();
  axios.post('http://localhost:5000/login', { email, password })
    .then(res => {
      navigate('/recommendation', {
          state: { jobs: res.data, user_email: email }
        });
      if (res.data.status === 'success') {
        sessionStorage.setItem('userEmail', email);
        
        axios.post('http://localhost:5000/notify-jobs', { user_input: email })
  .then(res => {
    console.log(res.data.message); 
  });

        
      } else {
        setError(res.data.message || "Login failed");
      }
    })
    .catch(err => {
      console.log(err);
      setError("Server error");
    });
};


  return (
    <div className="d-flex justify-content-center align-items-center vh-100"
    style={{backdropFilter: 'blur(16px) saturate(180%)', 
    WebkitBackdropFilter: 'blur(16px) saturate(180%)',backgroundColor: 'rgb(210, 226, 255)'}}>
      <div className="p-3 rounded w-25"
      style={{background:"white"}}>
      {error && (
        <div className="alert mt-3" style={{background: '#fd9a00'}} role="alert">
          {error}
        </div>
      )}
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <div className="mb-3">
            <label><strong>Email</strong></label>
            <input type="email" 
            placeholder="Enter Email" 
            className="form-control rounded-0"
            onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="mb-3">
            <label><strong>Password</strong></label>
            <input type="password" 
            placeholder="Enter Password" 
            className="form-control rounded-0"
            onChange={(e) => setPassword(e.target.value)} />
          </div>
          <button type="submit" className="btn btn-primary w-100 rounded-0">Login</button>
        </form>
        
        <p>Don't have an account?</p>
        <Link to="/sign" className="btn btn-default border w-100 rounded-0" 
        style={{ backgroundColor: 'white', color: 'black' }}
        onMouseEnter={(e) => e.target.style.backgroundColor = '#79df00'}
        onMouseLeave={(e) => e.target.style.backgroundColor = 'white'}>
        Signup
        </Link>
      </div>
    </div>
  );
}

export default Login;
