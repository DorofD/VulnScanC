import React, { createContext, useState, useEffect, useContext } from "react";

export const ColorSchemeContext = createContext();

export const ColorSchemeProvider = ({ children }) => {

    const getInitialScheme = () => {
        const saved = localStorage.getItem("colorScheme") || "default";
        return saved;
    };

    const [colorScheme, setColorScheme] = useState(getInitialScheme);

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', colorScheme);
    }, [colorScheme]);
    return (
        <ColorSchemeContext.Provider value={{ colorScheme, setColorScheme }}>
            {children}
        </ColorSchemeContext.Provider>
    );
}
