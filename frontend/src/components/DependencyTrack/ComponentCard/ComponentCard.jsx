import React, { Component } from "react";
import "./ComponentCard.css";


export default function ComponentCard({id, name, version, picked = false, onClick}) {
    if (!picked) {
        picked = "componentCard"
    } else {
        picked = "componentCardPicked"
    }
    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <div className="componentName">
                    <p className="componentName">{name}</p>
                </div>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Версия: </p>{version}
                </div>
            </div>
        </>
    )
}