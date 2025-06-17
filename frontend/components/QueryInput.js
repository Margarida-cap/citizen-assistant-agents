// components/QueryInput.js
import { useState } from 'react';
import { fetchIntent } from '../utils/api';

export default function QueryInput({ onIntent }) {
  const [query, setQuery] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    const intent = await fetchIntent(query);
    onIntent(intent);
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="What do you need?"
        style={{ width: '100%', padding: '0.5rem' }}
      />
      <button type="submit" style={{ marginTop: '0.5rem' }}>Submit</button>
    </form>
  );
}
