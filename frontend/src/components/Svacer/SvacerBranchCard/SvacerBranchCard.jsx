import React, { Component } from "react";
import "./SvacerBranchCard.css";


export default function SvacerBranchCard({id, name, onClick, picked = false}) {
    if (!picked) {
        picked = "svacerBranchCard"
    } else {
        picked = "svacerBranchCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <p className="svacerBranchCardName">{name}</p>
            </div>
        </>
    )
}