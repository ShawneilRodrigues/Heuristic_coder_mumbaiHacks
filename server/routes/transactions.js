const express = require('express');
const Transaction = require('../models/Transaction');
const jwt = require('jsonwebtoken');
const router = express.Router();

// Middleware to authenticate JWT token
const authenticateJWT = (req, res, next) => {
    const token = req.headers['authorization']?.split(' ')[1];
    if (!token) return res.sendStatus(403);

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) return res.sendStatus(403);
        req.user = user;
        next();
    });
};

// Create a new transaction
router.post('/', authenticateJWT, async (req, res) => {
    try {
        const { name, price, category } = req.body;
        const transaction = new Transaction({
            userId: req.user.userId,
            name,
            price,
            category
        });
        await transaction.save();
        res.status(201).json({ message: 'Transaction created successfully' });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// Get all transactions
router.get('/', authenticateJWT, async (req, res) => {
    try {
        const transactions = await Transaction.find({ userId: req.user.userId });
        res.json(transactions);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
