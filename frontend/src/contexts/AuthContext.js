import React, { useState, createContext } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setAuth] = useState(() => {
    return process.env.AUTH_VAR === '1';
  });
  const [userName, setUserName] = useState(`${process.env.AUTH_USER}`);
  const [userRole, setUserRole] = useState(`${process.env.AUTH_ROLE}`);
  const [userId, setUserId] = useState(1)
  const [accessToken, setaccessToken] = useState('')
  return (
    <AuthContext.Provider value={{ isAuthenticated, userName, userRole, userId, accessToken, toogleAuth: () => setAuth(prev => !prev), setUserName, setUserRole, setUserId, setaccessToken }}>
      {children}
    </AuthContext.Provider>
  );
};