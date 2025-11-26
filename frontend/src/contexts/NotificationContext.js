import React, { useState, createContext } from "react";

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  // Используем хук useState для создания переменной isAuthenticated и функции setAuth для ее изменения
  const [notificationData, setNotificationData] = useState({ message: '', type: '' });
  const [notificationToggle, toggleNote] = useState(0)

  // Возвращаем контекст провайдера, передавая значения isAuthenticated и setAuth в качестве значения контекста
  return (
    <NotificationContext.Provider value={{
      notificationData, notificationToggle, setNotificationData, toggleNotificationFunc: () => toggleNote(toggle => toggle + 1)
    }}>
      {children}
    </NotificationContext.Provider>
  );
};