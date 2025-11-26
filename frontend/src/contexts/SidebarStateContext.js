import React, { createContext, useState, useEffect, useContext } from "react";

export const SidebarStateContext = createContext();

export const SidebarStateProvider = ({ children }) => {

    const getInitialSidebarState = () => {
        const temp = localStorage.getItem("sidebar-state");
        // console.log('temp', temp)
        if (!temp) return false; // значение по умолчанию
        if (temp == 'default') return false;
        if (temp == 'collapsed') return true;
    };

    const [sidebarCollapsed, setSidebarCollapsed] = useState(getInitialSidebarState);

    useEffect(() => {
        console.log(sidebarCollapsed)
    }, [sidebarCollapsed]);

    return (
        <SidebarStateContext.Provider value={{ sidebarCollapsed, setSidebarCollapsed }}>
            {children}
        </SidebarStateContext.Provider>
    );
}
