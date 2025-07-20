import React, { useState } from 'react';
import axios from 'axios';

function JobUpdate() {
    const [title, setTitle] = useState('');
    const [company, setCompany] = useState('');
    const [description, setDescription] = useState('');
    const [skills, setSkills] = useState('');
    const [location, setLocation] = useState('');
    const [rank, setRank] = useState('');
    const [education, setEducation] = useState('');
    const [applyLink, setApplyLink] = useState('');
    const [dateOfPosting, setDateOfPosting] = useState('');
    const [lastDate, setLastDate] = useState('');
    
    const [formErrors, setFormErrors] = useState({});
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormErrors({});
        setSuccess('');

        const data = { title, company, description, education, skills, rank, location };

        try {
            const res = await axios.post('http://localhost:5000/jobupdate', data);
            if (res.status === 200) {
                setSuccess('Job Posted successfully');
                setTitle('');
                setCompany('');
                setDescription('');
                setSkills('');
                setLocation('');
                setRank('');
                setEducation('');
                setApplyLink('');
                setDateOfPosting('');
                setLastDate('');
                
            }
        } catch (err) {
            if (err.response && err.response.data.errors) {
                setFormErrors(err.response.data.errors);
            } else {
                console.error('Signup error:', err);
            }
        }
    };

    return (
        <div className="d-flex justify-content-center align-items-center px-3"
            style={{ background: 'linear-gradient(to bottom, #f5eff9, rgb(185, 230, 194))' }}>
            
           <div className="bg-white p-4 rounded shadow-lg w-10">
            {success && ( 
              <div className="alert alert-success">
                {success} <br/><a href="/searching" className="recommend-page">Recommendation Page</a>
              </div>
            )}
                <h2 className="text-center mb-4">Job Update</h2>
                <form onSubmit={handleSubmit}>
                    <Input label="Title" value={title} setValue={setTitle} />
                    <Input label="company" value={company} setValue={setCompany} error={formErrors.company} />
                    <Input label="description" type="description" value={description} setValue={setDescription} error={formErrors.description} />
                    <Input label="Skills" value={skills} setValue={setSkills} error={formErrors.skills} />
                    <Input label="Location" value={location} setValue={setLocation} error={formErrors.location} />
                    <Input label="Rank" value={rank} setValue={setRank} error={formErrors.rank} />
                    <Input label="Educational Qualification" value={education} setValue={setEducation} error={formErrors.education} />
                    <Input label="Apply Link" value={applyLink} setValue={setApplyLink} error={formErrors.applyLink} />
                    <Input label="Date of Posting" type="date" value={dateOfPosting} setValue={setDateOfPosting} error={formErrors.dateOfPosting} />  
                    <Input label="Last Date" type="date" value={lastDate} setValue={setLastDate} error={formErrors.lastDate} />
                    

                    <button type="submit" className="btn btn-success w-100 rounded-0">Submit</button>
                </form>
            </div>
        </div>
    );
}

function Input({ label, type = 'text', value, setValue, error }) {
    return (
        <div className="mb-3">
            <label className="form-label"><strong>{label}</strong></label>
            <input
                type={type}
                value={value}
                placeholder={`Enter your ${label}`}
                className={`form-control rounded-0 ${error ? 'is-invalid' : ''}`}
                onChange={(e) => setValue(e.target.value)}
            />
            {error && <div className="invalid-feedback">{error}</div>}
        </div>
    );
}

export default JobUpdate;
