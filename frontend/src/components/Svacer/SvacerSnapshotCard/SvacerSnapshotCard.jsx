import React, { Component } from "react";
import "./SvacerSnapshotCard.css";
import downloadLogo from './download.png'

export default function SvacerSnapshotCard({id, name, onClick, picked = false}) {
    if (!picked) {
        picked = "svacerSnapshotCard"
    } else {
        picked = "svacerSnapshotCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <div className="downloadLogo">

                <p className="svacerSnapshotCardName"> {name}</p> <img src={downloadLogo} alt="w" className="downloadLogo"/>
                </div>
            </div>
        </>
    )
}