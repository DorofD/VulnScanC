import React, { useEffect, useState } from "react";
import "./AiSummary.css";
import AiSummaryCard from "./AiSummaryCard/AiSummaryCard";
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

  

  return (
    <div className="aiSummaryMain">
      {isLoading && <div>Loading...</div>}
      {error && <div style={{ color: 'crimson' }}>{error}</div>}
      {!isLoading && !error && summary && (
        <div style={{ display: 'flex', gap: 16, width: '100%' }}>
          <div style={{ flex: 1 }}>
            <h3>Chat Nodes ({(summary.chat_nodes || []).length})</h3>
            {(summary.chat_nodes || []).map((n) => (
              <AiSummaryCard key={n.id || n.uuid} node={n} />
            ))}
          </div>
          <div style={{ flex: 1 }}>
            <h3>Embedding Nodes ({(summary.embedding_nodes || []).length})</h3>
            {(summary.embedding_nodes || []).map((n) => (
              <AiSummaryCard key={n.id || n.uuid} node={n} />
            ))}
          </div>
        </div>
      )}
      {!isLoading && !error && !summary && <div>No data</div>}
    </div>
  );
}
