import React, { useEffect, useState } from "react";
import "./AiSummary.css";
import { authFetch } from "../../services/authFetch";

export default function AiSummary() {
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      setIsLoading(true);
      setError("");
      try {
        const resp = await authFetch(`${process.env.BACKEND_URL}/ai/summary`, { method: "GET" });
        if (!resp.ok) {
          throw new Error(`Status ${resp.status}`);
        }
        const data = await resp.json();
        setSummary(data);
      } catch (e) {
        console.error(e);
        setError(String(e));
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, []);

  function renderNode(n) {
    const info = n.models || { success: false };
    return (
      <div className="card" key={n.id || n.uuid} style={{ marginBottom: 12 }}>
        <div style={{ fontWeight: 700 }}>{n.name || "(no name)"}</div>
        <div style={{ fontSize: 12, color: '#666' }}>{n.base_api_url}</div>
        <div style={{ marginTop: 8 }}>
          {info.success ? (
            <div>
              <div style={{ fontSize: 12, marginBottom: 6 }}>Models:</div>
              <ul style={{ margin: 0, paddingLeft: 18 }}>
                {(info.models || []).map((m) => (
                  <li key={m.get ? m.get('id') : (m.id || m.model_id || JSON.stringify(m))} style={{ fontSize: 13 }}>
                    {m.name || m.model_id || JSON.stringify(m)}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <div style={{ color: 'crimson' }}>unreachable / no models</div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="aiSummaryMain">
      {isLoading && <div>Loading...</div>}
      {error && <div style={{ color: 'crimson' }}>{error}</div>}
      {!isLoading && !error && summary && (
        <div style={{ display: 'flex', gap: 16, width: '100%' }}>
          <div style={{ flex: 1 }}>
            <h3>Chat Nodes ({(summary.chat_nodes || []).length})</h3>
            {(summary.chat_nodes || []).map(renderNode)}
          </div>
          <div style={{ flex: 1 }}>
            <h3>Embedding Nodes ({(summary.embedding_nodes || []).length})</h3>
            {(summary.embedding_nodes || []).map(renderNode)}
          </div>
        </div>
      )}
      {!isLoading && !error && !summary && <div>No data</div>}
    </div>
  );
}
