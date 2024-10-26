import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import Home from './components/Home';
import MainPage from './components/MainPage.jsx';
import About from './components/About.jsx';
import Contact from './components/Contact.jsx';
import Navbar from './components/Navbar.jsx';
import Login from './components/Login.jsx';
import Solutions from './components/Solutions.jsx';
import Signup from './components/Signup.jsx';
import Footer from './components/Footer.jsx';
import User from "./components/User.jsx"
const App = () => {
    return (


        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/about" element={<About />} />
                <Route path="/solutions" element={<Solutions />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/login" element={<Login />} /> {/* Route for Login */}
                <Route path="/signup" element={<Signup />} /> {/* Route for Signup */}
                <Route path="/user" element={<User />} /> {/* Route for Signup */}
            </Routes>
            <Footer/>
        </Router>
    );
};

export default App;
