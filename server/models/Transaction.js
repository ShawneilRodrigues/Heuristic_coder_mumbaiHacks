const mongoose = require('mongoose');

const transactionSchema = new mongoose.Schema({
    userId: {
        type: String,
        required: true,
    },
    name: {
        type: String,
        required: true,
    },
    price: {
        type: Number,
        required: true,
    },
    category: {
        type: String,
        required: true
    }
});

const Transaction = mongoose.model('Transaction', transactionSchema);

module.exports = Transaction;