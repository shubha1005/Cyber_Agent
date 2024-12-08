import React, { useState } from 'react';

const Port = () => {
  const [ip, setIp] = useState('');
  const [ports, setPorts] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async () => {
    try {
      const response = await fetch('http://localhost:5000/tool2/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ip,
          ports: ports.split(',').map(port => port.trim()),  // Convert ports to array
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResults(data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('An error occurred while communicating with the backend');
    }
  };

  return (
    <div>
      <h2>Port Scanner</h2>
      <input
        type="text"
        placeholder="Enter IP address"
        value={ip}
        onChange={(e) => setIp(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter ports (comma separated)"
        value={ports}
        onChange={(e) => setPorts(e.target.value)}
      />
      <button onClick={handleScan}>Scan</button>
      
      {results && (
        <div>
          <h3>Scan Results:</h3>
          <ul>
            {Object.entries(results).map(([port, status]) => (
              <li key={port}>{`Port ${port}: ${status}`}</li>
            ))}
          </ul>
        </div>
      )}

      {error && <div><h3 style={{ color: 'red' }}>Error: {error}</h3></div>}
    </div>
  );
};

export default Port;
