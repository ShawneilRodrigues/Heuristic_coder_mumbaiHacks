import React from 'react';
import { NavLink } from 'react-router-dom'; // Import NavLink
import './Navbar.css';
import EcoTrackLogo from './EcoTrackLogo';

const Navbar = () => {
    return (
        <nav className="navbar">
            <h1 className="logo"><EcoTrackLogo/></h1>
            <ul className="nav-links">
                <li>
                    <NavLink to="/" className={({ isActive }) => (isActive ? 'active' : '')}>Home</NavLink>
                </li>
                {/* <li> */}
                    {/* <NavLink to="/about" className={({ isActive }) => (isActive ? 'active' : '')}>About</NavLink> */}
                    {/* <a href="#about">About</a> */}
                {/* </li> */}
                {/* <li> */}
                    {/* <NavLink to="/solutions" className={({ isActive }) => (isActive ? 'active' : '')}>Solutions</NavLink> */}
                    {/* <a href="#solutions">Solutions</a> */}
                {/* </li> */}
                {/* <li> */}
                    {/* <NavLink to="/contact" className={({ isActive }) => (isActive ? 'active' : '')}>Contact</NavLink> */}
                    {/* <a href="#contact">Contact</a> */}
                {/* </li> */}
                <li>
                    <NavLink to="/login" className={({ isActive }) => (isActive ? 'active' : '')}>Log In</NavLink>
                </li>
                <li>
                    <NavLink to="/signup" className={({ isActive }) => (isActive ? 'active' : '')}>Sign Up</NavLink>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
