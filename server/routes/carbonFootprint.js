const express = require('express');
const Transaction = require('../models/Transaction');
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

// Calculate carbon footprint
router.get('/', authenticateJWT, async (req, res) => {
    try {
        // Fetch transactions for the authenticated user
        const transactions = await Transaction.find({ userId: req.user.userId });

        let carbonFootprint = 0;

        // Calculate carbon footprint based on categories
        transactions.forEach(transaction => {
            const price = transaction.price; // Accessing price from the schema
            const category = transaction.category; // Accessing category from the schema

            // Adjust the factors based on your requirements
            if (category === 'fuel') {
                carbonFootprint += price * 2.3; // Factor for fuel
            } else if (category === 'utilities') {
                carbonFootprint += price * 1.5; // Factor for utilities
            } else if (category === 'food') {
                carbonFootprint += price * 0.5; // Factor for food
            } else if (category === 'transport') {
                carbonFootprint += price * 0.8; // Factor for transport
            }
            // Add other categories and their corresponding factors as needed
        });

        // Send the calculated carbon footprint back in the response
        res.json({ carbonFootprint });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
