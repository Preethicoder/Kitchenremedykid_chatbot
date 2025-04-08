import React, { useState } from 'react';
import './App.css'; // Import the CSS file

function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: '👋 Hi! I can help with home remedies for your kid’s symptoms. What’s going on?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages.map(m => ({ role: m.role, content: m.content }))
        })
      });

      const data = await res.json();
      const aiMessage = { role: 'ai', content: data.answer };
      setMessages([...newMessages, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages([...newMessages, { role: 'ai', content: '❌ Oops! Something went wrong.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="app">
      <h1 className="title">🧑‍🍳 HomeCure-Kids Chatbot</h1>

      <div className="chat-container">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`message ${msg.role === 'user' ? 'user-message' : 'ai-message'}`}
          >
            {msg.content}
          </div>
        ))}
        {loading && <div className="loading">Typing...</div>}
      </div>

      <div className="input-container">
        <input
          className="input"
          type="text"
          placeholder="Describe your kid’s symptoms..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="send-button"
          onClick={sendMessage}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
