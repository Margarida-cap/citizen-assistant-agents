import React from 'react';
import ReactMarkdown from 'react-markdown';

const MessageList = ({ messages, userInfo }) => (
  <div className="message-list">
    {messages.map((m, i) => (
      <div
        key={i}
        className={`message-row ${m.from}`}
      >
        {m.from === 'agent' && (
          <div className="message-icon">
            <img
              src="/bot-avatar.png"
              alt="Bot"
              style={{ width: 32, height: 32, borderRadius: '50%' }}
            />
          </div>
        )}
        <div className={`message ${m.from}`}>
          {m.from === 'agent'
            ? <ReactMarkdown>{m.text}</ReactMarkdown>
            : m.text}
        </div>
        {m.from === 'user' && (
          <div className="message-icon">
            {userInfo?.picture ? (
              <img
                src={userInfo.picture}
                alt={userInfo.name || "User"}
                style={{ width: 32, height: 32, borderRadius: '50%' }}
              />
            ) : (
              // fallback icon
              <svg width="32" height="32" viewBox="0 0 24 24" fill="#1976d2">
                <circle cx="12" cy="8" r="4"/>
                <path d="M12 14c-4 0-7 2-7 4v2h14v-2c0-2-3-4-7-4z"/>
              </svg>
            )}
          </div>
        )}
      </div>
    ))}
  </div>
);

export default MessageList;