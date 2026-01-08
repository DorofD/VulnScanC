import React, { Component } from "react";
import "./ComponentCard.css";


export default function ComponentCard({id, name, status, license_number, osv_vuln_number, bdu_vuln_number, picked = false, onClick}) {
    return (
        <>
            <div id={id} className={!picked && "card component" || "card component picked"} onClick={onClick}>
                <p className="cardMainLabel">{name}</p>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Статус: </p>{status}
                    <p className="componentStatusFaded">Лицензии: </p>{license_number}
                </div>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Уязвимости OSV: </p>{osv_vuln_number}
                    <p className="componentStatusFaded">Уязвимости БДУ ФСТЭК: </p>{bdu_vuln_number}
                </div>
            </div>
        </>
    )
}