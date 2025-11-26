import React, { Component } from "react";
import Button from "../../Button/Button";
import "./LogCard.css";


export default function LogCard({ id, datetime, status, note, picked, onClick }) {
    let cardStyle
    let contentStyle

    if (!picked) {
        cardStyle = "card logs"
        contentStyle = "logContent"
    } else {
        cardStyle = "card logs picked"
        contentStyle = "logContentPicked"
    }

    return (

        <div id={id} className={cardStyle} onClick={!picked && onClick || (() => { })}>
            {picked &&
                <div className="logsCardClose">
                    <button onClick={onClick}>Закрыть</button>
                </div>}
            <p className="logDatetime">{datetime} {status === "ERROR" && <b>{status}</b> || <>{status}</>}</p>
            <div className={contentStyle}>{note}</div>
        </div>
    );
}