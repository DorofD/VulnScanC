import React, { Component } from "react";
import "./UserCard.css";


export default function UserCard({id, login, authType, role, onClick, picked = false}) {
    if (!picked) {
        picked = "userCard"
    } else {
        picked = "userCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>

                <p className="userName">{login}</p>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Роль: </p> {role} <p className="componentStatusFaded">Авторизация: </p>{authType}
                </div>
            </div>
        </>
    )
}