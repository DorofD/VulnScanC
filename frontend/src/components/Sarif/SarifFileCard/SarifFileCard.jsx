
import React, { Component } from "react";

export default function SarifFileCard({ id, name, onClick, picked = false, onClickButton }) {
    return (
        <>
            <div id={id} className={!picked && "card" || "card picked"} onClick={onClick}>
                <p className="cardMainLabel">{name}</p>
            </div>
        </>
    )
}