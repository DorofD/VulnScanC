import React, { Component } from "react";
import "./SnapshotCard.css";


export default function SnapshotCard({id, datetime, onClick, picked = false}) {
    if (!picked) {
        picked = "snapshotCard"
    } else {
        picked = "snapshotCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <p className="snapshotDatetime">{datetime}</p>
            </div>
        </>
    )
}