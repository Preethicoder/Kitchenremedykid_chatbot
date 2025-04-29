import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: '👋 Hi! I can help with home remedies for your kid’s symptoms. What’s going on?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatingPDF, setGeneratingPDF] = useState(false);

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
      let aiMessage;

      if (data.image_url) {
        aiMessage = { role: 'ai', content: data.answer, imageUrl: data.image_url };
      } else {
        aiMessage = { role: 'ai', content: data.answer, imageUrl: null };
      }

      setMessages([...newMessages, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages([...newMessages, { role: 'ai', content: '❌ Oops! Something went wrong.' }]);
    } finally {
      setLoading(false);
    }
  };

  const generatePDF = async () => {
  setGeneratingPDF(true);
  try {
    const res = await fetch('http://localhost:8000/generate_pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: messages.map(m => ({ role: m.role, content: m.content }))
      })
    });

    if (!res.ok) throw new Error('PDF generation failed');

    // Extract the filename from the Content-Disposition header
    const contentDisposition = res.headers.get('Content-Disposition');
    let filename = 'remedy.pdf';  // Fallback to a default filename
    console.log("Content-Disposition header:", contentDisposition);
    if (contentDisposition && contentDisposition.toLowerCase().includes('attachment')) {
    console.log("inside inseide")
      const matches = contentDisposition.match(/filename\*?=(?:UTF-8''|")?([^;\r\n"]+)/i);
      if (matches && matches[1]) {
        filename = decodeURIComponent(matches[1]);
        console.log("Decoded filename:", filename);
        console.log("inside")
      }
    }

    console.log('Filename extracted:', filename);  // For debugging

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);

    // Create a download link
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;  // <-- Use extracted filename here
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('PDF Error:', error);
    alert('Could not generate PDF. Try again later.');
  } finally {
    setGeneratingPDF(false);
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
            {msg.imageUrl && <img src={msg.imageUrl} alt="Generated Remedy" />}
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
        <button className="send-button" onClick={sendMessage} disabled={loading}>
          Send
        </button>
        <button className="send-button" onClick={generatePDF} disabled={generatingPDF}>
          {generatingPDF ? 'Creating PDF...' : 'Save as PDF'}
        </button>
      </div>
    </div>
  );
}

export default App;
