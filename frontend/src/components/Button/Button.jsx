import React from "react";
import "./Button.css"

export default function Button({ children, onClick, style, type, disabled = false}) {
    
    return <button className={style} onClick={onClick} type={type} disabled={disabled}>{children}</button>
}