import React from "react";
import "../AiLlamaNodeCard/AiLlamaNodeCard.css";

export default function LlamaNodeCard({ id, name, apiUrl, modelType, onClick, picked = false }) {
    return (
        <div id={id} className={!picked ? "card" : "card picked"} onClick={onClick}>
            <p className="cardMainLabel">{name}</p>
            <div className="llamaNodeStatus">
             <p className="llamaNodeStatusFaded">Базовый API URL: </p>{apiUrl}
            </div>
        </div>
    )
}
