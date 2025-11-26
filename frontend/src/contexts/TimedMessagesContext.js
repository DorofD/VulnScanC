import React, { useState, createContext, useRef } from "react";

export const TimedMessagesContext = createContext();

export const TimedMessagesProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const idRef = useRef(0);

  const addMessage = (text, style = 'info', duration = 10000) => {
    const id = idRef.current++;
    setMessages((msgs) => [...msgs, { id, text, style, duration }]);
    setTimeout(() => {
      setMessages((msgs) => msgs.filter((msg) => msg.id !== id));
    }, duration);
  };

  return (
    <TimedMessagesContext.Provider value={{ messages, addMessage }}>
      {children}
    </TimedMessagesContext.Provider>
  );
};