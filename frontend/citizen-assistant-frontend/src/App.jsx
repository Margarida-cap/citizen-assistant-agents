import React, { useState, useRef, useEffect } from 'react';
import ChatStreamDemo from './components/ChatComponent';
import ChatWindow from './components/ChatWindow';


const UserMenu = () => {
  const [open, setOpen] = useState(false);
  const menuRef = useRef();



  // Close menu if clicked outside
  useEffect(() => {
    const handleClick = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  return (
    <div ref={menuRef} style={{ position: 'absolute', top: 24, right: 32, zIndex: 100 }}>
      
      <button
        onClick={() => setOpen((o) => !o)}
        style={{
          background: '#fff',
          border: 'none',
          borderRadius: '50%',
          width: 44,
          height: 44,
          boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          padding: 0,
        }}
        aria-label="User menu"
      >
        {/* User SVG icon */}
        <svg width="28" height="28" viewBox="0 0 24 24" fill="#1976d2">
          <circle cx="12" cy="8" r="4"/>
          <path d="M12 14c-4 0-7 2-7 4v2h14v-2c0-2-3-4-7-4z"/>
        </svg>
      </button>
      {open && (
        <div
          style={{
            position: 'absolute',
            top: 50,
            right: 0,
            background: '#fff',
            borderRadius: 8,
            boxShadow: '0 4px 16px rgba(0,0,0,0.18)',
            minWidth: 180,
            padding: '0.5rem 0',
          }}
        >
          <div style={{ padding: '0.75rem 1.25rem', cursor: 'pointer', color: '#1976d2' }}>
            Profile
          </div>
          <div style={{ padding: '0.75rem 1.25rem', cursor: 'pointer', color: '#1976d2' }}>
            Settings
          </div>
          <div style={{ padding: '0.75rem 1.25rem', cursor: 'pointer', color: '#d32f2f' }}>
            Log out
          </div>
        </div>
      )}
    </div>
  );
};

const App = () => (
  <div style={{
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative'
  }}>
    <UserMenu />
    <h1 style={{
      color: '#fff',
      textAlign: 'center',
      marginTop: '2rem',
      marginBottom: '1.5rem',
      letterSpacing: '2px',
      textShadow: '0 2px 8px #000'
    }}>
      Citizen Assistant
      <ChatWindow />
    {/* <ChatStreamDemo /> */}
    </h1>
  </div>
);

export default App;
