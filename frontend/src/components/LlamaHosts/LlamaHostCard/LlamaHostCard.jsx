import React from "react";
import "./LlamaHostCard.css";

export default function LlamaHostCard({ id, name, apiUrl, modelType, onClick, picked = false }) {
    return (
        <div id={id} className={!picked ? "card users" : "card users picked"} onClick={onClick}>
            <p className="userName">{name}</p>
            <div className="componentStatus">
                <p className="componentStatusFaded">Тип модели: </p> {modelType} <p className="componentStatusFaded">API: </p>{apiUrl}
            </div>
        </div>
    )
}