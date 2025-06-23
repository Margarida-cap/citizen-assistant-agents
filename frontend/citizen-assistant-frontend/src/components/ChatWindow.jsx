import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import '../styles/chat.css';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const bottomRef = useRef(null);

  // Auto-scroll to newest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    setMessages((m) => [...m, { from: 'user', text }]);
    const reply = await fetchAgentResponse(text);
    setMessages((m) => [...m, { from: 'agent', text: reply }]);
  };

  const fetchAgentResponse = async (query) => {
    const res = await fetch('http://localhost:8001/messages/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_query: query })
    });
    const data = await res.json();
    return data.reply || JSON.stringify(data);
  };

  // Handle file upload
  const handleFileUpload = async (file) => {
    setMessages((m) => [...m, { from: 'user', text: `Sent file: ${file.name}` }]);
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch('http://localhost:8001/upload/', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    setMessages((m) => [...m, { from: 'agent', text: data.reply || 'File received.' }]);
  };

  // Drag and drop handlers
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragActive(true);
  };
  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragActive(false);
  };
  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  };

  return (
    <div
      className={`chat-window${dragActive ? ' drag-active' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <MessageList messages={messages} />
      <div ref={bottomRef} />
      <MessageInput onSend={sendMessage} />
      <div className="file-upload">
        <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
          <input
            type="file"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          <span className="file-upload-btn" style={{ display: 'flex', alignItems: 'center' }}>
            {/* Paperclip SVG icon */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="20"
              viewBox="0 0 24 24"
              width="20"
              style={{ marginRight: '6px', fill: '#fff' }}
            >
              <path d="M16.5,6.5v7c0,2.21-1.79,4-4,4s-4-1.79-4-4v-7c0-1.1,0.9-2,2-2s2,0.9,2,2v7c0,0.55-0.45,1-1,1s-1-0.45-1-1v-7H8.5v7
                c0,1.38,1.12,2.5,2.5,2.5s2.5-1.12,2.5-2.5v-7c0-1.93-1.57-3.5-3.5-3.5s-3.5,1.57-3.5,3.5v7c0,3.03,2.47,5.5,5.5,5.5
                s5.5-2.47,5.5-5.5v-7H16.5z"/>
            </svg>
            Attach File
          </span>
        </label>
      </div>
      {dragActive && (
        <div className="drag-overlay">
          <span>Drop file here to upload</span>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;
