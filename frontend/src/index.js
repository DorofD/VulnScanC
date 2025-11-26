// import React from "react";
// import ReactDOM from "react-dom/client"
// import App from "./components/App.jsx";
// import { BrowserRouter } from "react-router-dom"
// import { AuthProvider } from "./contexts/AuthContext.js";
// import { NotificationProvider  } from "./contexts/NotificationContext.js";
// import 'core-js/stable';
// import 'regenerator-runtime/runtime';


// const root = ReactDOM.createRoot(document.getElementById("root"));
// root.render(
//     <AuthProvider>
//         <NotificationProvider>
//             <BrowserRouter>
//                 <App />
//             </BrowserRouter> 
//         </NotificationProvider>
//     </AuthProvider>

// )
import React from "react";
import ReactDOM from "react-dom/client"
import App from "./components/App.jsx";
import { BrowserRouter } from "react-router-dom"
import { AuthProvider } from "./contexts/AuthContext.js";
import { NotificationProvider } from "./contexts/NotificationContext.js";
import { ColorSchemeProvider } from "./contexts/ColorSchemeContext.js";
import { TimedMessagesProvider } from "./contexts/TimedMessagesContext.js";
import { SidebarStateProvider } from "./contexts/SidebarStateContext.js";
import 'core-js/stable';
import 'regenerator-runtime/runtime';


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <ColorSchemeProvider>
        <AuthProvider>
            <SidebarStateProvider>
                <TimedMessagesProvider>
                    <NotificationProvider>
                        <BrowserRouter>
                            <App />
                        </BrowserRouter>
                    </NotificationProvider>
                </TimedMessagesProvider>
            </SidebarStateProvider>
        </AuthProvider>
    </ColorSchemeProvider>
)