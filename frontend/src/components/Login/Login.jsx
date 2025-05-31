import React from "react";
import { useState, useEffect } from "react";
import "./Login.css";
import Button from "../Button/Button";
import { useAuthContext } from "../../hooks/useAuthContext";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import { useNavigate } from 'react-router-dom';
import { apiAuth } from "../../services/apiLogin";

export default function Login() {
    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
    const { isAuthenticated, toogleAuth } = useAuthContext()
    const { userName, setUserName } = useAuthContext()
    const { userRole, setUserRole } = useAuthContext()
    const { userId, setUserId } = useAuthContext()
    const { accessToken, setaccessToken } = useAuthContext()
    const [status, setStatus] = useState('')
    const navigate = useNavigate();
    async function getAuth(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const formJson = Object.fromEntries(formData.entries());
        const username = formJson['username']
        const password = formJson['password']
        setStatus('loading')
        try {
            const response = await apiAuth(username, password)
            if (response.status == 200) {
                const user = await response.json()
                setUserName(user.body.login)
                setUserRole(user.body.role)
                setUserId(user.body.id)
                setaccessToken(user.access_token)
                localStorage.setItem('accessToken', user.access_token);
                toogleAuth()
                setNotificationData({ message: '', type: 'success' })
                toggleNotificationFunc()
                navigate('/');
            } else {
                setStatus('error')
                console.log('unauthorized')
            }


        } catch (err) {
            console.log(err)
            setStatus('error')
        }
    }
    useEffect(() => {
        if (isAuthenticated) {
            toogleAuth()
        }
        localStorage.removeItem('accessToken');
    }, [])

    return (
        <>
            <div className="login">
                <form className="login" onSubmit={getAuth}>
                    <input type="text" name="username" placeholder="username" />
                    <input type="password" name="password" placeholder="password" autoComplete="on" />
                    <Button style={"login"} type={"submit"}> Войти</Button>

                    {status === 'loading' && <div className="loading"> Ожидайте </div>}
                    {status === 'error' && <div className="error"> Не удалось войти </div>}
                </form>
            </div>
        </>
    );
}
