import React from 'react';
import EntryPage from './entrypage'; 
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchPage from './searchpage';
import Jobdetails from './jobdetails';
import Recommendation from './recommendation';
import Signup from './signup';
import JobUpdate from './jobForm';
import AllJobs from './allJobs';
import Login from './login';
import SignupLogin from './signupLogin';
import Pages from './usefulPages';

function App() {
  return (
    <BrowserRouter>
      <Routes>
      <Route path="/" element={<EntryPage />}/>
        <Route path="/searching" element={<SearchPage />}/>
        <Route path="/job/:id" element={<Jobdetails />}/>
        <Route path="/signuplogin" element={<SignupLogin/>}/>
        <Route path="/recommendation" element={<Recommendation />}/>
        <Route path="/sign" element={<Signup/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/jobupdate" element={<JobUpdate/>}/>
        <Route path="/alljob" element={<AllJobs/>}/>
        <Route path="/pages" element={<Pages/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
