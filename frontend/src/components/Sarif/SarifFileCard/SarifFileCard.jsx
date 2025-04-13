
import React, { Component } from "react";
import "./SarifFileCard.css";
import Button from "../../Button/Button";

export default function SarifFileCard({ id, name, onClick, picked = false, onClickButton }) {
    if (!picked) {
        picked = "sarifFileCard"
    } else {
        picked = "sarifFileCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <p className="sarifFileName">{name}</p>
            </div>
        </>
    )
}