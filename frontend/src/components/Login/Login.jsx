import React from "react";
import { useState, useEffect } from "react";
import "./Login.css";
import { useAuthContext } from "../../hooks/useAuthContext";
// // import { useNotificationContext } from "../../hooks/useNotificationContext";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";
import { useNavigate } from 'react-router-dom';
import { apiAuth } from "../../services/apiLogin";

export default function Login() {
    const { messages, addMessage } = useTimedMessagesContext();

    const { isAuthenticated, toogleAuth } = useAuthContext()
    const { userName, setUserName } = useAuthContext()
    const { userRole, setUserRole } = useAuthContext()
    const { userId, setUserId } = useAuthContext()
    const { accessToken, setaccessToken } = useAuthContext()
    const { userAuthType, setUserAuthType } = useAuthContext()
    const { userLdapInfo, setUserLdapInfo } = useAuthContext()
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
                setUserAuthType(user.body.auth_type)
                if (user.body.auth_type === 'ldap') {
                    // console.log(user.body.auth_type)
                    // console.log(user.body.displayName)
                    // console.log(user.body.givenName)
                    // console.log(user.body.sn)
                    // console.log(user.body.mail)
                    setUserLdapInfo({
                        displayName: user.body.displayName,
                        givenName: user.body.givenName,
                        sn: user.body.sn,
                        mail: user.body.mail,
                    })
                }
                setaccessToken(user.access_token)
                localStorage.setItem('accessToken', user.access_token);
                // console.log(userLdapInfo)
                toogleAuth()
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
                    <input className="login" type="text" name="username" placeholder="username" />
                    <input className="login" type="password" name="password" placeholder="password" autoComplete="on" />
                    <button className="login" type="submit">Войти</button>

                    {status === 'loading' && <div className="loading"> Ожидайте </div>}
                    {status === 'error' && <div className="loginError"> Не удалось войти </div>}
                </form>
            </div>
        </>
    );
}
