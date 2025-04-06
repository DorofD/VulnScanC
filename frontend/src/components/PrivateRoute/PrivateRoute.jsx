import React from "react";
import { useAuthContext } from "../../hooks/useAuthContext";
import { Outlet } from "react-router-dom";
import Login from "../Login/Login";


export const PrivateRoute = () => {

    const { isAuthenticated } = useAuthContext();
    if (isAuthenticated) {
        return <Outlet />
    } else {
        return <Login />;
    }
}