import React, { useState } from 'react';

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
    <div className="min-h-screen bg-orange-50 flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold text-orange-700 mb-4">🧑‍🍳 HomeCure-Kids Chatbot</h1>

      <div className="w-full max-w-xl bg-white shadow-lg rounded-2xl p-4 flex flex-col gap-3 overflow-y-auto h-[70vh]">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-xl max-w-xs ${
              msg.role === 'user' ? 'bg-orange-100 self-end' : 'bg-green-100 self-start'
            }`}
          >
            {msg.content}
          </div>
        ))}
        {loading && <div className="text-gray-400 italic self-start">Typing...</div>}
      </div>

      <div className="w-full max-w-xl mt-4 flex">
        <input
          className="flex-1 p-3 border border-orange-300 rounded-l-xl focus:outline-none"
          type="text"
          placeholder="Describe your kid’s symptoms..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="bg-orange-500 text-white px-4 rounded-r-xl hover:bg-orange-600"
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
