import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query.trim() }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Request failed');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResults(null);
    setError('');
  };

  return (
    <div className="p-3">
      <header className="px-5 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-center shadow-lg">
        <h1 className="text-3xl font-bold text-white">
          LLM-Powered Chatbot with FastAPI and SQL Integration
        </h1>
      </header>

      <main className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md mt-8">
        <div className="space-y-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your query(e.g., 'Show me all female customers from Pune')"
                className="w-full p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 resize-none"
                rows="4"
              />
              {loading && (
                <div className="absolute right-3 top-3">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                </div>
              )}
            </div>
            <div className="flex space-x-4">
              <button
                type="submit"
                className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50"
                disabled={loading || !query.trim()}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    Processing...
                  </span>
                ) : 'Search'}
              </button>
              <button
                type="button"
                onClick={handleClear}
                className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg disabled:opacity-50"
                disabled={loading}
              >
                Clear
              </button>
            </div>
          </form>
        </div>

        {error && (
          <div className="text-red-500 mb-5">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {results && (
          <div className="mt-5">
            <div>
              <h2>Results</h2>
              <p>{results.message}</p>
            </div>

            <div>
              <h3>Generated SQL Query:</h3>
              <code>{results.generated_sql}</code>
            </div>

            {results.results && results.results.length > 0 ? (
              <div>
                <h3>Customer Data:</h3>
                <table className="w-full border border-gray-300">
                  <thead>
                    <tr>
                      <th className="border border-gray-300 p-2 bg-gray-100">ID</th>
                      <th className="border border-gray-300 p-2 bg-gray-100">Name</th>
                      <th className="border border-gray-300 p-2 bg-gray-100">Gender</th>
                      <th className="border border-gray-300 p-2 bg-gray-100">Location</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.results.map((customer, index) => (
                      <tr key={index}>
                        <td className="border border-gray-300 p-2">{customer.customer_id}</td>
                        <td className="border border-gray-300 p-2">{customer.name}</td>
                        <td className="border border-gray-300 p-2">{customer.gender}</td>
                        <td className="border border-gray-300 p-2">{customer.location}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div>
                <p>No customers found matching your query.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;