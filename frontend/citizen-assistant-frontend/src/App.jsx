import React, { useState, useRef, useEffect } from 'react';
import Login from './components/Login';
import ChatWindow from './components/ChatWindow';
import { decodeJwt } from './utils/jwt';

const UserMenu = ({ userInfo }) => {
  const [open, setOpen] = React.useState(false);
  const menuRef = React.useRef();

  React.useEffect(() => {
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
        {userInfo?.picture ? (
          <img
            src={userInfo.picture}
            alt={userInfo.name}
            style={{ width: 36, height: 36, borderRadius: '50%' }}
          />
        ) : (
          // fallback icon
          <svg width="28" height="28" viewBox="0 0 24 24" fill="#1976d2">
            <circle cx="12" cy="8" r="4"/>
            <path d="M12 14c-4 0-7 2-7 4v2h14v-2c0-2-3-4-7-4z"/>
          </svg>
        )}
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
            minWidth: 220,
            padding: '0.5rem 0',
          }}
        >
          <div style={{ padding: '1rem', borderBottom: '1px solid #eee', textAlign: 'center' }}>
            {userInfo?.picture && (
              <img
                src={userInfo.picture}
                alt={userInfo.name}
                style={{ width: 48, height: 48, borderRadius: '50%', marginBottom: 8 }}
              />
            )}
            <div style={{ fontWeight: 'bold', color: '#222' }}>{userInfo?.name}</div>
            <div style={{ fontSize: '0.95em', color: '#555' }}>{userInfo?.email}</div>
          </div>
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

const App = () => {
  const [idToken, setIdToken] = useState(null);
  const [userInfo, setUserInfo] = useState(null);

  const handleLogin = (token) => {
    setIdToken(token);
    setUserInfo(decodeJwt(token));
  };

  if (!idToken) {
    return <Login onLogin={handleLogin} />;
  }
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative'
    }}>
      <UserMenu userInfo={userInfo} />
      <h1 style={{
        color: '#fff',
        textAlign: 'center',
        marginTop: '2rem',
        marginBottom: '1.5rem',
        letterSpacing: '2px',
        textShadow: '0 2px 8px #000'
      }}>
        Citizen Assistant
      </h1>
      <ChatWindow idToken={idToken} userInfo={userInfo} />
    </div>
  );
};

export default App;
