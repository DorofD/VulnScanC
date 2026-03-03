import React from "react";
import "../AiLlamaNodeCard/AiLlamaNodeCard.css";

export default function LlamaNodeCard({ id, name, apiUrl, modelType, isNodeActive, onClick, picked = false }) {
    return (
        <div id={id} className={!picked ? "card" : "card picked"} onClick={onClick}>
            <p className="cardMainLabel">{name} {isNodeActive && 'active' || ''}</p>
            <div className="llamaNodeStatus">
             <p className="llamaNodeStatusFaded">Базовый API URL: </p>{apiUrl}
            </div>
        </div>
    )
}
