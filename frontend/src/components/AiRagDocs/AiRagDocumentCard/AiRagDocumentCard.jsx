import React from "react";
import "./AiRagDocumentCard.css";

export default function AiRagDocumentCard({ id, name, filePath, onClick, picked = false, children }) {
  return (
    <div id={id} className={!picked ? "card" : "card picked"} onClick={onClick}>
      <p className="cardMainLabel">{name}</p>
      <div className="ragDocCardPath">{filePath}</div>
      {children}
    </div>
  );
}
