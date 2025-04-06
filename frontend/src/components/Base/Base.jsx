import React, { Component, useState, useEffect } from "react";
import "./Base.css";
import { NavLink as NavLinkBase, Outlet, useLocation } from "react-router-dom";
import Button from "../Button/Button";
import Notification from "../Notification/Notification";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import { useAuthContext } from "../../hooks/useAuthContext";
import Loader from "../Loader/Loader";

const NavLink = React.forwardRef((props, ref) => {
    return (
        <NavLinkBase
            ref={ref}
            {...props}
        />
    );
});

export default function Base() {
    const { isAuthenticated, toogleAuth } = useAuthContext();
    const { userName, userRole } = useAuthContext();
    const { notificationData } = useNotificationContext();
    const location = useLocation();

    return (
        <>
            <div className="baseHeader" id="modal-root">
                {userName}
                <Button style={"logout"} type={"submit"} onClick={toogleAuth}> Выйти </Button>
            </div>
            <div className="baseSidebar">
                <nav className="baseSidebar">
                    <Notification data={notificationData} />
                    <ul className="base">
                        <li>
                            <NavLink to="/" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                Проекты
                            </NavLink>
                        </li>
                        <li>
                            <NavLink to="/components" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                Компоненты
                            </NavLink>
                        </li>
                        <li>
                            <NavLink to="/snapshots" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                Снапшоты
                            </NavLink>
                        </li>
                        <li>
                            <NavLink to="/bdu_fstec" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                БДУ ФСТЭК
                            </NavLink>
                        </li>
                        <li>
                            <NavLink to="/svacer" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                Svacer
                            </NavLink>
                        </li>
                        <li>
                            <NavLink to="/dependencyTrack" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                Dependency-Track
                            </NavLink>
                        </li>
                        <li>
                            <NavLink to="/sarif" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                Sarif Viewer
                            </NavLink>
                        </li>
                        {userRole === 'admin' && (
                            <li>
                                <NavLink to="/admin" className={({ isActive }) => isActive ? 'activeBaseHref' : 'baseHref'}>
                                    Администрирование
                                </NavLink>
                            </li>
                        )}
                        <li>
                            <NavLink
                                to="/about"
                                className={({ isActive }) =>
                                    isActive || location.pathname.startsWith('/docs') ||
                                        location.pathname.startsWith('/ui_instructions') ||
                                        location.pathname.startsWith('/web_ui') ||
                                        location.pathname.startsWith('/executable_module') ||
                                        location.pathname.startsWith('/README')
                                        ? 'activeBaseHref'
                                        : 'baseHref'
                                }
                            >
                                О приложении
                            </NavLink>
                        </li>
                    </ul>
                </nav>
            </div>
            <div className="baseContent">
                <Outlet />
            </div>
        </>
    );
}


// const NavLink = React.forwardRef((props, ref) => {
//     return (
//       <NavLinkBase
//         ref={ref}
//         {...props}
//         className={({ isActive }) =>
//           isActive ? 'activeBaseHref' : 'baseHref'
//         }
//       />
//     );
//   });

// export default function Base() {
//     const { isAuthenticated, toogleAuth} = useAuthContext()
//     const {userName, userRole} = useAuthContext()
//     const {notificationData} = useNotificationContext()


//     return (
//         <>
//             <div className="baseHeader" id="modal-root">
//                 {userName}
//                 <Button style={"logout"} type={"submit"} onClick={toogleAuth}> Выйти </Button>
//             </div>
//             <div className="baseSidebar">
//                 <nav className="baseSidebar">
//                 <Notification data={notificationData}/>
//                     <ul className="base">
//                         <li > <NavLink to="/" >Проекты</NavLink></li>
//                         <li> <NavLink to="/components" >Компоненты</NavLink></li>
//                         <li> <NavLink to="/snapshots" >Снапшоты</NavLink></li>
//                         <li> <NavLink to="/svacer" >Svacer</NavLink></li>
//                         {userRole === 'admin' && <>
//                         <li> <NavLink to="/admin" >Администрирование</NavLink></li>
//                         </>}
//                         <li> <NavLink to="/about">О приложении</NavLink></li>
//                     </ul>
//                 </nav>
//             </div>
//             <div className="baseContent">
//                 <Outlet />
//             </div>
//         </>
//     );
// }
