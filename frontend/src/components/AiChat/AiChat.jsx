import React, { useMemo, useRef, useState, useEffect } from "react";
import { apiAiChatSendMessage } from "../../services/apiAi";
import { apiGetChatNodes } from "../../services/apiLlamaNodes";
import "./AiChat.css";
// import "../AiChat/AiChat.css"


export default function AiChat() {
  const [systemPrompt, setSystemPrompt] = useState("");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastResponse, setLastResponse] = useState(null);
  const [showRawResponse, setShowRawResponse] = useState(false);
  const [useRag, setUseRag] = useState(false);

  const abortRef = useRef(null);
  const listRef = useRef(null);

  const displayMessages = useMemo(() => {
    // system обычно не показывают в чате, но можно
    return messages.filter((m) => m.role !== "system");
  }, [messages]);

  function scrollToBottom() {
    requestAnimationFrame(() => {
      if (!listRef.current) return;
      listRef.current.scrollTop = listRef.current.scrollHeight;
    });
  }

  function onKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }


  async function send() {
    const text = input.trim();
    if (!text || isLoading) return;
    setError("");
    const historyWithoutOldSystem = messages.filter((m) => m.role !== "system");
    const nextMessages = [...historyWithoutOldSystem, { role: "user", content: text }];

    setMessages(nextMessages);
    setInput("");
    setIsLoading(true);
    scrollToBottom();
    try {
      const res = await apiAiChatSendMessage(nextMessages, useRag);

      if (!res.ok) {
        const body = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status}: ${body || res.statusText}`);
      }

      const data = await res.json();
      console.log(data)
      const assistant = data?.choices?.[0]?.message?.content ?? "";
      console.log(assistant)

      setMessages((prev) => [...prev, { role: "assistant", content: assistant }]);
      setLastResponse(data);
      scrollToBottom();
    } catch (e) {
      if (e.name === "AbortError") {
        setError("Остановлено пользователем.");
      } else {
        setError(e.message || "Ошибка запроса");
      }
    } finally {
      setIsLoading(false);
      abortRef.current = null;
    }
  }

  function resetChat() {
    setError("");
    setIsLoading(false);
    setSystemPrompt("")
    setMessages([{ role: "system", content: systemPrompt }]);
    setLastResponse(null);
  }

  // useEffect(() => {
    
  // }, []);

  function CollapsibleJson({ data, name }) {
    const [open, setOpen] = useState(false);

    if (data === null || typeof data !== "object") {
      return (
        <div className="jsonRow">
          <span className="jsonKey">{name}:</span>
          <span className="jsonValue">{String(data)}</span>
        </div>
      );
    }

    const entries = Array.isArray(data)
      ? data.map((v, i) => [i, v])
      : Object.entries(data);

    return (
      <div className="jsonNode">
        <div className="jsonSummary" onClick={() => setOpen((s) => !s)}>
          <button>{open ? "−" : "+"}</button>
          <span className="jsonKey">{name}</span>
          <span className="jsonMeta">{Array.isArray(data) ? ` [${data.length}]` : ""}</span>
        </div>
        {open && (
          <div className="jsonChildren">
            {entries.map(([k, v]) => (
              <CollapsibleJson key={String(k)} name={String(k)} data={v} />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <>
    <div className="chatRagShell">
      <header className="chatRagHeader">
        <div className="chatRagTitle">
          Чат с AI
        </div>

        <div className="chatRagControls">
        <label className="chatRagCheckbox" style={{ marginLeft: 12 }}>
          <input
            type="checkbox"
            checked={useRag}
            onChange={(e) => setUseRag(e.target.checked)}
            disabled={isLoading}
          />
          <span className="checkbox-box" />
          Использовать RAG
        </label>
          <button onClick={resetChat} disabled={isLoading}>
            Удалить контекст
          </button>
        </div>
      </header>


      <main className="chatRagMain" ref={listRef}>
        {displayMessages.length === 0 ? (
          <div className="emptyState">Напишите сообщение, чтобы начать.</div>
        ) : (
          displayMessages.map((m, idx) => (
            <div
            key={idx}
            className={[
              "msgRow",
              m.role === "user" ? "msgUser" : "",
              m.role === "assistant" ? "msgAssistant" : "",
            ].join(" ")}
            >
              <div className="msgMeta">{m.role}</div>
              <div className="msgBubble">
                <pre className="msgText">{m.content}</pre>
              </div>
            </div>
          ))
        )}

        {isLoading && (
          <div className="msgRow msgAssistant">
            <div className="msgMeta">assistant</div>
            <div className="msgBubble">
              <div className="typing">Обработка запроса</div>
            </div>
          </div>
        )}
      </main>

      {error && <div className="errorBox">{error}</div>}

      <footer className="chatRagFooter">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Введите сообщение… (Enter — отправить, Shift+Enter — новая строка)"
          rows={3}
          disabled={isLoading}
          />
        <button onClick={send} disabled={isLoading || !input.trim()}>
          Отправить
        </button>
      </footer>
    </div>
    <div className="chatRagInfoContainer">
      {lastResponse ? (
        <div className="jsonPanel">
          <div className="jsonHeader">
            <strong>Last response</strong>
            <div className="jsonHeaderControls">
              <button onClick={() => setShowRawResponse((s) => !s)}>{showRawResponse ? "Hide raw" : "Show raw"}</button>
              <button onClick={() => { setLastResponse(null); setShowRawResponse(false); }}>Clear</button>
            </div>
          </div>
          {showRawResponse ? (
            <pre className="jsonPre">{JSON.stringify(lastResponse, null, 2)}</pre>
          ) : (
            <div className="jsonTree">
              <CollapsibleJson name="response" data={lastResponse} />
            </div>
          )}
        </div>
      ) : (
        <div className="emptyState">Подробный вывод</div>
      )}
    </div>
          </>
  );
}
