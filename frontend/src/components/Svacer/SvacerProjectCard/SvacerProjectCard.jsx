import React, { Component } from "react";
import "./SvacerProjectCard.css";


export default function SvacerProjectCard({id, name, onClick, picked = false}) {
    if (!picked) {
        picked = "svacerProjectCard"
    } else {
        picked = "svacerProjectCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <p className="svacerProjectCardName">{name}</p>
            </div>
        </>
    )
}