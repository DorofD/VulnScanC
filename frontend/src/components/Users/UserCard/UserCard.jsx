import React, { Component } from "react";
import "./UserCard.css";


export default function UserCard({ id, login, authType, role, onClick, picked = false }) {

    return (
        <>
            <div id={id} className={!picked && "card users" || "card users picked"} onClick={onClick}>

                <p className="userName">{login}</p>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Роль: </p> {role} <p className="componentStatusFaded">Авторизация: </p>{authType}
                </div>
            </div>
        </>
    )
}