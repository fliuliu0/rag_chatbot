import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import gemLogo from './assets/gem-logo.svg';

function App() {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'bot',
      text: 'Welcome to GEM Chatbot! Ask me anything about GEM.',
    },
  ]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const chatEndRef = useRef(null);

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    setChatHistory((prev) => [...prev, { sender: 'user', text: userInput }]);
    setUserInput('');
    setIsBotTyping(true);

    try {
      const response = await axios.post('http://localhost:5001/query', {
        query: userInput,
      });

      const botResponse = response.data.answer || "I couldn't provide an answer.";
      setChatHistory((prev) => [...prev, { sender: 'bot', text: botResponse }]);
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        { sender: 'bot', text: 'Oops! Something went wrong. Please try again.' },
      ]);
    } finally {
      setIsBotTyping(false);
    }
  };

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory]);

  return (
    <div className="App">
      <div className="logo-container">
        <img src={gemLogo} alt="GEM Logo" className="gem-logo" />
        
      </div>
      <div className="chat-container">
        <div className="chat-window">
          <div className="chat-history">
            {chatHistory.map((message, index) => (
              <div
                key={index}
                className={`message ${message.sender === 'user' ? 'user' : 'bot'} ${
                  index === 0 ? 'welcome' : ''
                }`}
              >
                {message.text}
              </div>
            ))}
            {isBotTyping && (
              <div className="message bot">
                <em>Bot is typing...</em>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
          <div className="chat-input">
            <input
              type="text"
              placeholder="Type your message..."
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              aria-label="Type your message"
            />
            <button onClick={sendMessage} aria-label="Send message">
              Send
            </button>
          </div>
        </div> 
      </div>
    </div>
  );
}

export default App;
