import React, { useState, useRef } from "react";
import "./TimedMessages.css";
import { useTimedMessagesContext } from "../../hooks/useTimedMessagesContext";


export default function TimedMessages() {
    const { messages, addMessage } = useTimedMessagesContext();
    return (
        <div className="tmc-messages">
            {messages.map((msg) => (
                <div key={msg.id} className={msg.style && `tmc-message ${msg.style}` || "tmc-message "}
                    style={{ '--animation-duration': `${msg.duration}ms` }}
                >
                    {msg.text}
                </div>
            ))}
        </div>
    );
}