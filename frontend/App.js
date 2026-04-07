import React, { useState } from 'react';

function App() {
  const [longUrl, setLongUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleShorten = async (port) => {
    setLoading(true);
    try {
      // You can toggle between 8001 and 8002 to show the distributed nature!
      const response = await fetch(`http://localhost:${port}/shorten`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ long_url: longUrl }),
      });
      const data = await response.json();
      setShortUrl(data.short_url);
    } catch (err) {
      alert("Error connecting to the API instance");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-8">Distributed URL Shortener</h1>
      <div className="w-full max-w-md bg-gray-800 p-6 rounded-lg shadow-xl">
        <input 
          type="text" 
          placeholder="Paste your long URL here..." 
          className="w-full p-3 rounded bg-gray-700 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={longUrl}
          onChange={(e) => setLongUrl(e.target.value)}
        />
        <div className="flex gap-2">
          <button 
            onClick={() => handleShorten(8001)}
            className="flex-1 bg-blue-600 hover:bg-blue-700 p-3 rounded font-semibold transition"
          >
            Use Instance 1 (8001)
          </button>
          <button 
            onClick={() => handleShorten(8002)}
            className="flex-1 bg-green-600 hover:bg-green-700 p-3 rounded font-semibold transition"
          >
            Use Instance 2 (8002)
          </button>
        </div>
        
        {shortUrl && (
          <div className="mt-6 p-4 bg-gray-900 border border-gray-700 rounded text-center">
            <p className="text-sm text-gray-400 mb-1">Your Short Link:</p>
            <a href={shortUrl} target="_blank" className="text-blue-400 hover:underline break-all font-mono">
              {shortUrl}
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;