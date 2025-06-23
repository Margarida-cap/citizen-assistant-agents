import React from 'react';

const MessageList = ({ messages }) => (
  <div className="message-list">
    {messages.map((m, i) => (
      <div key={i} className={`message ${m.from}`}>
        {m.text}
      </div>
    ))}
  </div>
);

export default MessageList;
