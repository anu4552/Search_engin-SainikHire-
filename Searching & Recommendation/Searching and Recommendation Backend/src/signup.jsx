import React, { useState } from 'react';
import axios from 'axios';
import { Link} from 'react-router-dom';

function Signup() {
    const [form, setForm] = useState({
        name: '',
        email: '',
        password: '',
        education: '',
        skills: '',
        rank: '',
        location: ''
    });
    const [formErrors, setFormErrors] = useState({});
    const [success, setSuccess] = useState('');


    const handleChange = (field) => (e) => {
        setForm({ ...form, [field]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormErrors({});
        setSuccess('');

        try {
            const res = await axios.post('http://localhost:5000/signup', form);
            if (res.status === 200) {
                setSuccess('Signup successful!');
                setForm({
                    name: '',
                    email: '',
                    password: '',
                    education: '',
                    skills: '',
                    rank: '',
                    location: ''
                });
                
            }
        } catch (err) {
            if (err.response?.data?.errors) {
                setFormErrors(err.response.data.errors);
            } else {
                console.error('Signup error:', err);
            }
        }
    };

    return (
        <div className="d-flex justify-content-center"
            style={{ background: 'linear-gradient(to bottom, #f5eff9, rgb(185, 230, 194))' }}>
            <div className="bg-white p-4 rounded shadow-lg w-25">
                {success && (
                    <div className="alert alert-success">
                        {success} <br />
                        <a href="/login" className="recommend-page">Recommendation Page</a>
                    </div>
                )}
                <h2 className="text-center mb-4">Information</h2>
                <form onSubmit={handleSubmit}>
                    <Input label="Name" value={form.name} setValue={handleChange('name')} error={formErrors.name} />
                    <Input label="Rank" value={form.rank} setValue={handleChange('rank')} error={formErrors.rank} />
                    <Input label="Educational Qualification" value={form.education} setValue={handleChange('education')} error={formErrors.education} />
                    <Input label="Skills" value={form.skills} setValue={handleChange('skills')} error={formErrors.skills} />
                    <Input label="Location" value={form.location} setValue={handleChange('location')} error={formErrors.location} />
                    <Input label="Email" type="email" value={form.email} setValue={handleChange('email')} error={formErrors.email} />
                    <Input label="Password" type="password" value={form.password} setValue={handleChange('password')} error={formErrors.password} />

                    <button type="submit" className="btn btn-success w-100 rounded-0">Submit</button>
                </form>
                <p>Already have an account?</p>
                <Link
                    to="/login"
                    className="btn w-100 rounded-0"
                    style={{ backgroundColor: 'white', color: 'black' }}
                    onMouseEnter={e => e.target.style.backgroundColor = '#04bade'}
                    onMouseLeave={e => e.target.style.backgroundColor = 'white'}
                >
                    Login
                </Link>
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
                onChange={setValue}
            />
            {error && <div className="invalid-feedback">{error}</div>}
        </div>
    );
}

export default Signup;
