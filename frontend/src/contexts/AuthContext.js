import React, {useState, createContext} from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setAuth] = useState(() => {
      // Преобразуем строковое значение в булево
      return process.env.AUTH_VAR === '1';
    });
    const [userName, setUserName] = useState(`${process.env.AUTH_USER}`);
    const [userRole, setUserRole] = useState(`${process.env.AUTH_ROLE}`);
    const [userId, setUserId] = useState(1)
    return (
      <AuthContext.Provider value={{ isAuthenticated, userName, userRole, userId, toogleAuth: () => setAuth(prev => !prev), setUserName, setUserRole, setUserId}}>
        {children}
      </AuthContext.Provider>
    );
};