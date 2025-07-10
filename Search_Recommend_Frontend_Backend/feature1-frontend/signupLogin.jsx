import React from 'react';
import { Link } from 'react-router-dom';

function SignupLogin() {
  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        background: '#eccffc',
      }}
    >
      <div
        style={{
          display: 'flex',
          gap: '40px',
          padding: '40px',
        }}
      >
        <div
          style={{
            width: '250px',
            height: '180px',
            background: '#d5cfff',
            borderRadius: '12px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
          }}
        >
          <h4 style={{ color: '#5e35b1', marginBottom: '20px' }}>New User?</h4>
          <Link to="/sign" className="btn btn-primary px-4 py-2 rounded-pill">
            Sign Up
          </Link>
        </div>

        <div
          style={{
            width: '250px',
            height: '180px',
            background: '#ffdbe9',
            borderRadius: '12px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
          }}
        >
          <h4 style={{ color: '#c2185b', marginBottom: '20px' }}>Already Registered?</h4>
          <Link to="/login" className="btn btn-danger px-4 py-2 rounded-pill">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}

export default SignupLogin;
