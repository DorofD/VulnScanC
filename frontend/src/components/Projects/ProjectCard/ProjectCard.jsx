import React, { Component } from "react";
// import "./ProjectCard.css";


export default function ProjectCard({ id, name, onClick, picked = false }) {

    return (
        <>
            <div id={id} className={!picked && "card" || "card picked"} onClick={onClick}>
                <p className="cardMainLabel">{name}</p>
            </div>
        </>
    )
}