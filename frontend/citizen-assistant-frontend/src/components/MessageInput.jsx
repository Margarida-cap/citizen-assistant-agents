import React, { useState } from 'react';
const MessageInput = ({ onSend, disabled }) => {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  return (
    <div className="message-input">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Ask something..."
        disabled={disabled}
      />
      <button onClick={handleSend} disabled={disabled}>
        Send
      </button>
    </div>
  );
};


export default MessageInput;
