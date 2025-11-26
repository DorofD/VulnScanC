import React, { Component } from "react";
import "./Admin.css"
import { NavLink as NavLinkAdmin, Outlet } from "react-router-dom";

import { useColorScheme } from "../../hooks/useColorThemeContext";
import { useSidebarState } from "../../hooks/useSidebarStateContext";

import UsersGearIcon from "../../svg_images/UsersGear.svg"
import ConfluenceIcon from "../../svg_images/Confluence.svg"
// import BareMetalIcon from "../../svg_images/BareMetal.svg"
import CatalogIcon from "../../svg_images/Catalog.svg"
import PythonGearIcon from "../../svg_images/PythonGear.svg"
import RocketChatIcon from "../../svg_images/RocketChat.svg"

const NavLink = React.forwardRef((props, ref) => {
  return (
    <NavLinkAdmin
      ref={ref}
      {...props}
      className={({ isActive }) =>
        // isActive ? 'activeAdminHref' : 'adminHref'
        isActive ? 'baseHref active' : 'baseHref'
      }
    />
  );
});

export default function Admin() {
  const { colorScheme } = useColorScheme();
  const { sidebarCollapsed } = useSidebarState();

  return (
    <>
      <div className={!sidebarCollapsed && "baseSidebar" || "baseSidebar collapsed"}>
        <nav className={!sidebarCollapsed && "baseSidebar" || "baseSidebar collapsed"}>
          <NavLink to="/admin/users" >
            {!sidebarCollapsed &&
              <div className="baseHrefText">Пользователи</div>
              ||
              <UsersGearIcon className="baseSidebarIcon"></UsersGearIcon>}
            {sidebarCollapsed && <div className="baseSidebarTextDiv">Пользователи</div>}
          </NavLink>
          <NavLink to="/admin/binary" >
            {!sidebarCollapsed &&
              <div className="baseHrefText">Исполняемый модуль</div>
              ||
              <ConfluenceIcon className="baseSidebarIcon"></ConfluenceIcon>}
            {sidebarCollapsed && <div className="baseSidebarTextDiv">Исполняемый модуль</div>}
          </NavLink>
          <NavLink to="/admin/logs" >
            {!sidebarCollapsed &&
              <div className="baseHrefText">Логи</div>
              ||
              <CatalogIcon className="baseSidebarIcon"></CatalogIcon>}
            {sidebarCollapsed && <div className="baseSidebarTextDiv">Логи</div>}
          </NavLink>
        </nav>
      </div>
      <div className={!sidebarCollapsed && "baseContent" || "baseContent collapsed"}>
        <Outlet />
      </div>
    </>
  );
}