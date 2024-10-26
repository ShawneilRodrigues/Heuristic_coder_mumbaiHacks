const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');

const authenticateJWT = (req, res, next) => {
    const token = req.headers['authorization']?.split(' ')[1];
    if (!token) return res.sendStatus(403);

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) return res.sendStatus(403);
        req.user = user;
        next();
    });
};

// Get suggestions for reducing carbon footprint
router.get('/', authenticateJWT, (req, res) => {
    const suggestions = [
        "Consider using public transportation or carpooling.",
        "Switch to energy-efficient appliances.",
        "Reduce meat consumption.",
        "Use renewable energy sources where possible.",
        "Minimize single-use plastic purchases."
    ];
    res.json({ suggestions });
});

module.exports = router;
