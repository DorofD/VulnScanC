import React from "react";
import "./Button.css"

export default function Button({ children, onClick, style, type}) {
    
    return <button className={style} onClick={onClick} type={type}>{children}</button>
}