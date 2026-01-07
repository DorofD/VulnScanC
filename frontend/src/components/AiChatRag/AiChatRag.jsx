import React, { useMemo, useRef, useState } from "react";
import { apiRagChatSendMessage } from "../../services/apiAi";
import "./AiChatRag.css";
// import "../AiChat/AiChat.css"


export default function AiChatRag() {
  const [systemPrompt, setSystemPrompt] = useState("");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    // { role: "system", content: "Ты специалист по DevSecOps, отвечай строго на основе CONTEXT, если в CONTEXT нет ответа - так и скажи" },
    // { role: "user", content: "CONTEXT: [chunk 1 | source: ГОСТ Р 56939—2024 | section: Введение (стр. 3) | chunk_id: gostr56939-2024_intro_p3_c01] Настоящий стандарт направлен"}
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

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
      const res = await apiRagChatSendMessage(nextMessages);

      if (!res.ok) {
        const body = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status}: ${body || res.statusText}`);
      }

      const data = await res.json();
      console.log(data)
      const assistant = data?.choices?.[0]?.message?.content ?? "";
      console.log(assistant)

      setMessages((prev) => [...prev, { role: "assistant", content: assistant }]);
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
  }

  return (
    <div className="chatRagShell">
      <header className="chatRagHeader">
        <div className="chatRagTitle">
          Обработка запросов с использованием RAG
        </div>

        <div className="chatRagControls">
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
  );
}
