import React, { Component, useState, useEffect } from "react";
import "./Base.css";
import { NavLink as NavLinkBase, Outlet, useLocation } from "react-router-dom";
import TimedMessages from "../TimedMessages/TimedMessages";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import { useAuthContext } from "../../hooks/useAuthContext";
import { useSidebarState } from "../../hooks/useSidebarStateContext";
import ColorSchemeSelector from "../ColorSchemeSelector/ColorSchemeSelector";
import HomeIcon from "../../svg_images/Home.svg"
import ScheduleIcon from "../../svg_images/Schedule.svg"
import GearIcon from "../../svg_images/Gear.svg"
import ManualIcon from "../../svg_images/Manual.svg"
import ExpandRightIcon from "../../svg_images/ExpandRight.svg"
import ExpandLeftIcon from "../../svg_images/ExpandLeft.svg"
import LogoutIcon from "../../svg_images/Logout.svg"
import UserIcon from "../../svg_images/User.svg"
import BareMetalIcon from "../../svg_images/BareMetal.svg"
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
    const { userName, userRole, userId, userAuthType, userLdapInfo, accessToken } = useAuthContext();
    const { messages, addMesage } = useTimedMessagesContext();
    const { sidebarCollapsed, setSidebarCollapsed } = useSidebarState();
    const [userHintActive, setUserHintActive] = useState(false);
    // const location = useLocation();
    useEffect(() => {
        const mediaQuery = window.matchMedia('(min-width: 992px)');

        const handleMediaChange = (e) => {
            if (!e.matches) {
                localStorage.setItem("sidebar-state", 'collapsed')
                setSidebarCollapsed(true)
            }

        };

        handleMediaChange(mediaQuery);

        mediaQuery.addEventListener('change', handleMediaChange);

        return () => {
            mediaQuery.removeEventListener('change', handleMediaChange);
        };
    }, []);

    return (
        <>
            <div className="baseHeader" id="modal-root">
                <ColorSchemeSelector></ColorSchemeSelector>
                <div className={userHintActive && "baseUserIconContainer activated" || "baseUserIconContainer"}>
                    <UserIcon className="baseUserIconStyle" onClick={() => setUserHintActive((prev) => !prev)} />
                </div>
                <div className="baseUserName">
                    {userAuthType === 'ldap' && `${userLdapInfo.givenName} ${userLdapInfo.sn[0]}.` || userName}
                </div>
                {userHintActive && userAuthType === 'ldap' && <div className="baseUsernameTooltip">
                    <b>{userLdapInfo.displayName}</b>
                    <div className="base-param-row">
                        <div className="base-param-key">Логин</div>
                        <div>{userName}</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">E-mail</div>
                        <div>{userLdapInfo.mail}</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">Аутентификация</div>
                        <div>LDAP</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">Роль</div>
                        <div>{userRole}</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">ID в сервисе</div>
                        <div>{userId}</div>
                    </div>
                </div>}
                {userHintActive && userAuthType === 'local' && <div className="baseUsernameTooltip">
                    <b>{userName}</b>
                    <div className="base-param-row">
                        <div className="base-param-key">Логин</div>
                        <div>{userName}</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">E-mail</div>
                        <div>Отсутствует</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">Аутентификация</div>
                        <div>Локальная</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">Роль</div>
                        <div>{userRole}</div>
                    </div>
                    <div className="base-param-row">
                        <div className="base-param-key">ID в сервисе</div>
                        <div>{userId}</div>
                    </div>
                </div>}
                <div className="baseLogoutIconContainer" onClick={toogleAuth}><LogoutIcon className='baseLogoutIconStyle '></LogoutIcon></div>
            </div>
            <div className="baseBody">
                <div className={!sidebarCollapsed && "baseSidebar" || "baseSidebar collapsed"}>
                    <TimedMessages data={messages} />
                    <nav className={!sidebarCollapsed && "baseSidebar" || "baseSidebar collapsed"}>
                        <NavLink to="/" className={({ isActive }) => isActive ? 'baseHref active' : 'baseHref'}>
                            {!sidebarCollapsed &&
                                <div className="baseHrefText">Проекты</div>
                                ||
                                <HomeIcon className="baseSidebarIcon"></HomeIcon>} {sidebarCollapsed && <div className="baseSidebarTextDiv">Проекты</div>}
                        </NavLink>
                        <NavLink to="/components" className={({ isActive }) => isActive ? 'baseHref active' : 'baseHref'} aria-current="page">
                            {!sidebarCollapsed &&
                                <div className="baseHrefText">Компоненты</div>
                                ||
                                <BareMetalIcon className="baseSidebarIcon"></BareMetalIcon>} {sidebarCollapsed && <div className="baseSidebarTextDiv">Компоненты</div>}
                        </NavLink>
                        <NavLink to="/snapshots" className={({ isActive }) => isActive ? 'baseHref active' : 'baseHref'} aria-current="page">
                            {!sidebarCollapsed &&
                                <div className="baseHrefText">Снапшоты</div>
                                ||
                                <ScheduleIcon className="baseSidebarIcon"></ScheduleIcon>} {sidebarCollapsed && <div className="baseSidebarTextDiv">Снапшоты</div>}
                        </NavLink>
                        {userRole === 'admin' && (<>
                            <NavLink to="/admin" className={({ isActive }) => isActive ? 'baseHref active' : 'baseHref'}>
                                {!sidebarCollapsed &&
                                    <div className="baseHrefText">Администрирование</div>
                                    ||
                                    <GearIcon className="baseSidebarIcon"></GearIcon>} {sidebarCollapsed && <div className="baseSidebarTextDiv">Администрирование</div>}
                            </NavLink>
                        </>)}
                        <NavLink to="/about" className={({ isActive }) => isActive ? 'baseHref active' : 'baseHref'}>
                            {!sidebarCollapsed &&
                                <div className="baseHrefText">О приложении</div>
                                ||
                                <ManualIcon className="baseSidebarIcon"></ManualIcon>} {sidebarCollapsed && <div className="baseSidebarTextDiv">О приложении</div>}
                        </NavLink>
                    </nav>
                    {!sidebarCollapsed &&
                        <div className="baseSidebarExpandContainer" onClick={() => { localStorage.setItem("sidebar-state", 'collapsed'); setSidebarCollapsed(true) }}>
                            <ExpandLeftIcon className="baseSidebarExpandIcon" ></ExpandLeftIcon>
                        </div>
                        ||
                        <div className="baseSidebarExpandContainer" onClick={() => { localStorage.setItem("sidebar-state", 'default'); setSidebarCollapsed(false) }}>
                            <ExpandRightIcon className="baseSidebarExpandIcon" ></ExpandRightIcon>
                        </div>
                    }
                </div>
                <div className={!sidebarCollapsed && "baseContent" || "baseContent collapsed"}>
                    <Outlet />
                </div>
            </div>
        </>
    );
}
