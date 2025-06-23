import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/chat.css';  // import any global CSS here
import './styles/global.css';

// Create a root and render <App />
ReactDOM
  .createRoot(document.getElementById('root'))
  .render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
