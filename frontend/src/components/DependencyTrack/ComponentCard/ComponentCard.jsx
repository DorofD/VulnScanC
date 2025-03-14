import React, { Component } from "react";
import "./ComponentCardDT.css";


export default function ComponentCard({id, name, version, picked = false, onClick}) {
    if (!picked) {
        picked = "componentCardDT"
    } else {
        picked = "componentCardPickedDT"
    }
    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <div className="componentNameDT">
                    <p className="componentNameDT">{name}</p>
                </div>
                <div className="componentStatusDT">
                    <p className="componentStatusFadedDT">Версия: </p>{version}
                </div>
            </div>
        </>
    )
}