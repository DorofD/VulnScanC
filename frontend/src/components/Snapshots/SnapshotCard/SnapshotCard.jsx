import React, { Component } from "react";
import "./SnapshotCard.css";


export default function SnapshotCard({id, datetime, onClick, picked = false}) {
    return (
        <>
            <div id={id} className={!picked && "card snapshot" || "card snapshot picked"} onClick={onClick}>
                <p className="userName">{datetime}</p>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Snapshot</p>
                </div>
            </div>
        </>
    )
}