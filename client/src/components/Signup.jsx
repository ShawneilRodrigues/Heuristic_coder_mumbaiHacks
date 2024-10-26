import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './Auth.css'; 

const Signup = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleChange = (e) => {
        const { id, value } = e.target;
        setFormData((prevFormData) => ({
            ...prevFormData,
            [id]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/auth/signup', {
                name: formData.username,
                email: formData.email,
                password: formData.password,
            });
            setSuccessMessage(response.data.message);
            setError('');
            navigate('/user'); 
        } catch (error) {
            setError(error.response?.data?.error || 'Signup failed');
        }
    };

    return (
        <div className="auth-container">
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input type="text" id="username" required value={formData.username} onChange={handleChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input type="email" id="email" required value={formData.email} onChange={handleChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" required value={formData.password} onChange={handleChange} />
                </div>
                <button type="submit">Sign Up</button>
            </form>
            {successMessage && <p className="success-message">{successMessage}</p>}
            {error && <p className="error-message">{error}</p>}
            <p className="switch-auth">
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    );
};

export default Signup;
