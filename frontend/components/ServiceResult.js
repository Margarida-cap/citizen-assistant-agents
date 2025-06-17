// components/ServiceResult.js
import { fetchService } from '../utils/api';

export default function ServiceResult({ intent, onService }) {
  if (!intent) return null;

  const handleClick = async () => {
    const service = await fetchService(intent.service_id);
    onService(service);
  };

  return (
    <div style={{ marginBottom: '1rem' }}>
      <h2>Detected Intent: {intent.intent}</h2>
      <button onClick={handleClick}>Fetch Service</button>
    </div>
  );
}
