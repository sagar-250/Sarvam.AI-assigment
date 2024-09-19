import React, { useState, useRef, useEffect } from 'react';
import { Card, Input, Button, List, Avatar, Spin, Switch } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined, SyncOutlined } from '@ant-design/icons';
import axios from 'axios';
import './ChatWindow.css'; // Custom CSS for additional styling

const { TextArea } = Input;

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRagMode, setIsRagMode] = useState(false);  // State to manage toggle between RAG and agent modes
  const messagesEndRef = useRef(null);  // Ref to track the bottom of the message list

  // Function to scroll to the bottom of the message list
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // useEffect to trigger scroll to bottom when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSpeak = (text) => {
    if (!window.speechSynthesis) {
      alert('Your browser does not support speech synthesis.');
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.7  ;
    window.speechSynthesis.speak(utterance);
  };

  const handleSubmit = async () => {
    if (inputText.trim()) {
      const date = new Date();
      const strTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      const userMessage = {
        text: <pre style={{
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word',
          overflow: 'auto',
          maxWidth: '100%',
          
        }}>{inputText}</pre>,
        time: strTime,
        sender: 'user',
      };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInputText('');

      try {
        setIsLoading(true);
        const endpoint = isRagMode ? 'http://127.0.0.1:8000/rag/query' : 'http://127.0.0.1:8000/agent/query';
        const response = await axios.post(endpoint, {
          query: inputText,
        });

        const botMessage = {
          text: <pre style={{
            whiteSpace: 'pre-wrap',
            wordWrap: 'break-word',
            overflow: 'auto',
            maxWidth: '100%',
          }}>
            {response.data.Response}
            </pre> || 'Sorry, I didn’t understand that.',
          time: strTime,
          sender: 'bot',
        };
        handleSpeak(response.data.Response)
        console.log(response.data.Response);
        
        
        

        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error('Error with bot API:', error);
        const errorMessage = {
          text: 'Sorry, there was an issue connecting to the bot.',
          time: strTime,
          sender: 'bot',
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      } finally {
        setIsLoading(false);
        
      }
    }
  };

  const handleToggle = (checked) => {
    setIsRagMode(checked);  // Update state based on toggle switch
  };

  return (
    <div className="chat-container">
      <Card
        title={<div style={{ color: "white" }}>Bot</div>}
        bordered={false}
        className='chat-box'
        style={{ width: 500, color: '#fff' }} // Dark blue background
      >
        <div className="toggle-container">
          <span style={{ color: '#fff', marginRight: '10px', fontWeight:'bold' }}>
            {isRagMode ? 'RAG Mode' : 'Agent Mode'}
          </span>
          <Switch
            checkedChildren="RAG"
            unCheckedChildren="Agent"
            checked={isRagMode}
            onChange={handleToggle}
            style={{
              backgroundColor: isRagMode ? '#6b08c7' : '#F59E0B',  // Change color based on mode
              borderColor: isRagMode ? '#6b08c7' : '#F59E0B',
            }}
          />
        </div>

        <div className="message-list-container">
          <List
            className="message-list"
            itemLayout="horizontal"
            dataSource={messages}
            renderItem={(msg, index) => (
              <List.Item
                key={index}  // Ensure a unique key for each message
                className={msg.sender === 'user' ? 'user-message' : 'bot-message'}
                style={{
                  justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <List.Item.Meta
                  avatar={
                    msg.sender === 'user' ? (
                      <Avatar icon={<UserOutlined />} style={{ backgroundColor: '#860ff6', color: '#fff' }} />
                      ) : (
                        <Avatar icon={<RobotOutlined />} style={{ backgroundColor: '#F59E0B', color: '#fff' }} />
                      )
                  }
                  title={msg.sender === 'user' ? 'You' : <div>{isRagMode?'RAG Bot':'Agent Bot'}</div>}
                  description={<div style={{ color: "white" }}>{msg.text}<div ref={messagesEndRef}/></div>}
                  style={{
                    color: '#fff',
                    backgroundColor: msg.sender === 'user' ? '#860ff6' : '#374151',
                    borderRadius: '10px',
                    padding: '10px',
                    marginBottom: '5px',
                    maxWidth: '70%',
                  }}
                />
                <span className="message-time" style={{ color: '#D1D5DB',margin:"2px" }}>{msg.time}</span>
              </List.Item>
            )}
          />
          {/* Div to track the end of the message list */}
        </div>

        {isLoading && (
          <div className="loading-container">
            <Spin size="small" style={{ color: '#fff' }} /> <span style={{ color: '#fff' }}>Bot is typing...</span>
          </div>
        )}

        <TextArea
          rows={2}
          placeholder="Type your message..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onPressEnter={handleSubmit}
          style={{
            backgroundColor: '#374151',
            color: '#fff',
            borderRadius: '5px',
            marginBottom: '10px',
          }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={handleSubmit}
          disabled={isLoading}
          style={{ width: '100%', backgroundColor: '#6b08c7', borderColor: '#1D4ED8' }}
        >
          Send
        </Button>
      </Card>
    </div>
  );
};

export default ChatWindow;
