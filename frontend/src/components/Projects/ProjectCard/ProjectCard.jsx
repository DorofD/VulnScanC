import React, { Component } from "react";
import "./ProjectCard.css";


export default function ProjectCard({id, name, onClick, picked = false}) {
    if (!picked) {
        picked = "projectCard"
    } else {
        picked = "projectCardPicked"
    }

    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <p className="name">{name}</p>
            </div>
        </>
    )
}