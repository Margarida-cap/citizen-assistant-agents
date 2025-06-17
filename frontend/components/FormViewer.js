// components/FormViewer.js
import { useEffect, useState } from 'react';
import { fetchAutoFill } from '../utils/api';

export default function FormViewer({ service }) {
  const [fields, setFields] = useState(null);

  useEffect(() => {
    if (!service) return;
    const user_profile = { name: 'Alice', passport_no: 'X1234567' };
    fetchAutoFill(service.url, user_profile).then(data => setFields(data.fields));
  }, [service]);

  if (!service) return null;

  return (
    <div>
      <h3>Service: {service.title}</h3>
      {fields ? (
        <ul>
          {Object.entries(fields).map(([k, v]) => (
            <li key={k}><strong>{k}:</strong> {v}</li>
          ))}
        </ul>
      ) : (
        <p>Loading form...</p>
      )}
    </div>
  );
}
