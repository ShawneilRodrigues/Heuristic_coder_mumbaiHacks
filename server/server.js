const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const authRoutes = require('./routes/auth');
const transactionRoutes = require('./routes/transactions');
const carbonFootprintRoutes = require('./routes/carbonFootprint');
const suggestionsRoutes = require('./routes/suggestions');
const cors = require('cors');

dotenv.config();
const app = express();

app.use(cors({
    origin: 'http://localhost:3000'
}));

app.use(express.json());

const userRoutes = require('./routes/user');
app.use('/user', userRoutes);

app.use('/auth', authRoutes);
app.use('/transactions', transactionRoutes);
app.use('/carbon-footprint', carbonFootprintRoutes);
app.use('/suggestions', suggestionsRoutes);

mongoose
    .connect(process.env.DATABASE.replace('<db_password>', process.env.DATABASE_PASSWORD))
    .then(() => console.log('Connected to MongoDB'))
    .catch((error) => console.error('MongoDB connection error:', error));

app.get('/', (req, res) => {
    res.send('Server is running!');
});
    
app.listen(process.env.PORT, () => {
    console.log(`Server running on port ${process.env.PORT}`);
});
