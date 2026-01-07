import React, { useMemo, useRef, useState } from "react";
import "./AiChat.css";

const API_URL = "http://192.168.1.133:8080/v1/chat/completions";

export default function AiChat() {
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

  function stop() {
    if (abortRef.current) {
      abortRef.current.abort();
      abortRef.current = null;
    }
  }

  async function send() {
    const text = input.trim();
    if (!text || isLoading) return;

    setError("");

    // синхронизируем system в истории
    const base = [{ role: "system", content: systemPrompt.trim() || "Ты помощник" }];
    const historyWithoutOldSystem = messages.filter((m) => m.role !== "system");
    const nextMessages = [...base, ...historyWithoutOldSystem, { role: "user", content: text }];

    setMessages(nextMessages);
    setInput("");
    setIsLoading(true);
    scrollToBottom();

    const controller = new AbortController();
    abortRef.current = controller;
    console.log(nextMessages)
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: controller.signal,
        body: JSON.stringify({
          model: "local",
          messages: nextMessages,
          temperature: 0.2,
          max_tokens: 300,
          stream: false
        }),
      });

      if (!res.ok) {
        const body = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status}: ${body || res.statusText}`);
      }

      const data = await res.json();
      const assistant = data?.choices?.[0]?.message?.content ?? "";

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
    stop();
    setSystemPrompt("")
    setMessages([{ role: "system", content: systemPrompt }]);
  }

  return (
    <div className="chatShell">
      <header className="chatHeader">
        <div className="chatTitle">Подключение к API LLM сервиса напрямую</div>
        
        <div className="chatControls">
          <button onClick={resetChat} disabled={isLoading}>
            Очистить
          </button>
          <button onClick={stop} disabled={!isLoading}>
            Прервать действие
          </button>
        </div>
      </header>

      <section className="systemBox">
        <input
          value={"URL: " + API_URL}
          onChange={(e) => setSystemPrompt(e.target.value)}
          placeholder="URL"
          // disabled={isLoading}
          disabled={true}
        />
      </section>
      <section className="systemBox">
        <input
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          placeholder="Системный промпт (роль)"
          disabled={isLoading}
        />
      </section>

      <main className="chatMain" ref={listRef}>
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
              <div className="typing">Думаю…</div>
            </div>
          </div>
        )}
      </main>

      {error && <div className="errorBox">{error}</div>}

      <footer className="chatFooter">
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
