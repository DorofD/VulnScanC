import React, { Component } from "react";
import "./Admin.css"
import { NavLink as NavLinkAdmin, Outlet } from "react-router-dom";

const NavLink = React.forwardRef((props, ref) => {
    return (
      <NavLinkAdmin
        ref={ref}
        {...props}
        className={({ isActive }) =>
          isActive ? 'activeAdminHref' : 'adminHref'
        }
      />
    );
  });

export default function Admin() {
    return (
        <>
            <div className="admin-sidebar">
                <nav className="admin-sidebar">
                    <ul className="admin">
                        <li className="admin"> <NavLink to="/admin/users" >Пользователи</NavLink></li>
                        <li className="admin"> <NavLink to="/admin/binary" >Исполняемый модуль</NavLink></li>
                        <li className="admin"> <NavLink to="/admin/logs" >Логи</NavLink></li>
                        <li className="admin"> <NavLink to="/admin/svacer" >Svacer</NavLink></li>
                        <li className="admin"> <NavLink to="/admin/ldap" >LDAP</NavLink></li>
                    </ul>
                </nav>
            </div>
            <div className="admin-content">
                <Outlet />
            </div>
        </>
    );
}