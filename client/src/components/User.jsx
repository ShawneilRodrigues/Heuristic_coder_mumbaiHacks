import React, { useState } from 'react';
import axios from 'axios';
import './User.css'; // Import the CSS file for styling

const ProductForm = () => {
  const [productName, setProductName] = useState('');
  const [productCost, setProductCost] = useState('');
  const [category, setCategory] = useState('food');
  const [responseMessage, setResponseMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const data = {
      productName,
      productCost,
      category,
    };

    console.log('Submitting data:', data); // Log the data being sent

    try {
      const response = await axios.post('https://320b-61-246-51-230.ngrok-free.app/analyze', data);
      console.log('Response received:', response.data); // Log the response
      setResponseMessage(response.data);
    } catch (error) {
      console.error('Error submitting the product data:', error);
      setResponseMessage('Error submitting data: ' + error.message); // Show error message
    }

    // Reset the form fields
    setProductName('');
    setProductCost('');
    setCategory('food');
  };

  return (
    <div>
      <form className="product-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="productName">Product Name:</label>
          <input
            type="text"
            id="productName"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="productCost">Product Cost:</label>
          <input
            type="number"
            id="productCost"
            value={productCost}
            onChange={(e) => setProductCost(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="category">Category:</label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="food">Food</option>
            <option value="fuel">Fuel</option>
            <option value="energy">Energy</option>
            <option value="travel">Travel</option>
          </select>
        </div>
        <button type="submit">Submit</button>
      </form>
      {responseMessage && (
        <div className="response-message">
          <h3>Response:</h3>
          <pre>{JSON.stringify(responseMessage, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ProductForm;
