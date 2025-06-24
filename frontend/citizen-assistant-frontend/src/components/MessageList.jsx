import React from 'react';

const userIcon = (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="#1976d2">
    <circle cx="12" cy="8" r="4"/>
    <path d="M12 14c-4 0-7 2-7 4v2h14v-2c0-2-3-4-7-4z"/>
  </svg>
);

const agentIcon = (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="#43a047">
    <circle cx="12" cy="8" r="4"/>
    <rect x="6" y="14" width="12" height="6" rx="3"/>
  </svg>
);

const MessageList = ({ messages }) => (
  <div className="message-list">
    {messages.map((m, i) => (
      <div
        key={i}
        className={`message-row ${m.from}`}
      >
        {m.from === 'agent' && (
          <div className="message-icon">{agentIcon}</div>
        )}
        <div className={`message ${m.from}`}>
          {m.text}
        </div>
        {m.from === 'user' && (
          <div className="message-icon">{userIcon}</div>
        )}
      </div>
    ))}
  </div>
);

export default MessageList;