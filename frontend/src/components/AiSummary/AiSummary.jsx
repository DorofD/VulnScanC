import React, { useMemo, useRef, useState } from "react";
import "./AiSummary.css";

export default function AiSummary() {
  const [systemPrompt, setSystemPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");



  return (
    <div className="aiSummaryMain">
    отображение состояния сервисов
    </div>
  );
}
