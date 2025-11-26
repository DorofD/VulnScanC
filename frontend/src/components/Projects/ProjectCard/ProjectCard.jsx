import React, { Component } from "react";
import "./ProjectCard.css";


export default function ProjectCard({ id, name, onClick, picked = false }) {

    return (
        <>
            <div id={id} className={picked && "card project picked" || "card project"} onClick={onClick}>
                <div className="projectCardHeader">
                    <p className="projectCardName">{name}</p>
                </div>
            </div>
        </>
    )
}