// pages/index.js
import { useState } from 'react';
import QueryInput from '../components/QueryInput';
import ServiceResult from '../components/ServiceResult';
import FormViewer from '../components/FormViewer';

export default function Home() {
  const [intent, setIntent] = useState(null);
  const [service, setService] = useState(null);

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '1rem' }}>
      <h1>Citizen Assistant Demo</h1>
      <QueryInput onIntent={setIntent} />
      <ServiceResult intent={intent} onService={setService} />
      <FormViewer service={service} />
    </div>
  );
}
