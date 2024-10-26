// routes/user.js
const express = require('express');
const router = express.Router();
const authenticateJWT = require('../middlewares/authMiddleware');  // Import the middleware

// Protect this route with the authenticateJWT middleware
router.get('/', authenticateJWT, (req, res) => {
    // Access req.user if needed
    res.json({ message: `Welcome, user ${req.user.userId}!` });
});

module.exports = router;