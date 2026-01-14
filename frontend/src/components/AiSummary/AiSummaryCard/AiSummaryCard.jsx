import React from "react";
import "../AiSummaryCard/AiSummaryCard.css";

export default function AiSummaryCard({ node }) {
  const info = node.models || { success: false };

  return (
    <div className="card aiSummaryCard">
      <div className="cardMainLabel">{node.name || "(no name)"}</div>
      <div className="aiSummaryApi">{node.base_api_url}</div>

      <div style={{ marginTop: 8 }}>
        {info.success ? (
          <div>
            <div className="modelsLabel">Models:</div>
            <ul className="modelsList">
              {(info.models || []).map((m) => (
                <li key={m.get ? m.get("id") : (m.id || m.model_id || JSON.stringify(m))} className="modelItem">
                  <div className="modelName">{m.name || m.model_id || JSON.stringify(m)}</div>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div className="unreachable">unreachable / no models</div>
        )}
      </div>
    </div>
  );
}
