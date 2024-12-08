import React, { useState } from 'react';

const Cryptography = () => {
  const [text, setText] = useState('');
  const [key, setKey] = useState('');
  const [method, setMethod] = useState('AES');  // Default to AES
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Function to handle encryption
  const handleEncrypt = async () => {
    try {
      const response = await fetch('http://localhost:5000/tool1/encrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          key,
          method,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.result);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('An error occurred while communicating with the backend');
    }
  };

  // Function to handle decryption
  const handleDecrypt = async () => {
    try {
      const response = await fetch('http://localhost:5000/tool1/decrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: result,  // Decrypt the result of the encryption
          key,
          method,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.result);  // Display decrypted result
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('An error occurred while communicating with the backend');
    }
  };

  return (
    <div>
      <h2>Cryptography Tool</h2>
      <input
        type="text"
        placeholder="Enter text"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter key"
        value={key}
        onChange={(e) => setKey(e.target.value)}
      />
      <select value={method} onChange={(e) => setMethod(e.target.value)}>
        <option value="AES">AES</option>
        <option value="DES">DES</option>
        <option value="RSA">RSA</option>
      </select>

      {/* Encrypt Button */}
      <button onClick={handleEncrypt}>Encrypt</button>

      {/* Decrypt Button (Only show after encryption) */}
      {result && <button onClick={handleDecrypt}>Decrypt</button>}

      {/* Display result */}
      {result && <div><h3>Result: {result}</h3></div>}
      
      {/* Display error */}
      {error && <div><h3 style={{ color: 'red' }}>Error: {error}</h3></div>}
    </div>
  );
};

export default Cryptography;
