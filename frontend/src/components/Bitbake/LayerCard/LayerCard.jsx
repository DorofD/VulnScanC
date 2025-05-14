import React, { Component } from "react";
import "./LayerCard.css";


export default function LayerCard({ id, name, onClick, picked = false }) {
    if (!picked) {
        picked = "layerCard"
    } else {
        picked = "layerCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <p className="name">{name}</p>
            </div>
        </>
    )
}