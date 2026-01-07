import React, { useMemo, useRef, useState } from "react";
import "./AiRagConf.css";

export default function AiRagConf() {
  const [systemPrompt, setSystemPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");



  return (
    <div className="ragConfMain">
    загрузка документов, нарезка на чанки, эмбеддинг
    </div>
  );
}
