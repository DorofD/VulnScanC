import React, { Component } from "react";
import "./ComponentCard.css";


export default function ComponentCard({id, name, status, license_number, osv_vuln_number, bdu_vuln_number, picked = false, onClick}) {
    if (!picked) {
        picked = "componentCard"
    } else {
        picked = "componentCardPicked"
    }
    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <div className="componentName">
                    <p className="componentName">{name}</p>
                </div>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Статус: </p>{status}
                    <p className="componentLicenseFaded">Лицензии: </p>{license_number}
                </div>
                <div className="componentStatus">
                    <p className="componentStatusFaded">Уязвимости OSV: </p>{osv_vuln_number}
                    <p className="componentLicenseFaded">Уязвимости БДУ ФСТЭК: </p>{bdu_vuln_number}
                </div>
            </div>
        </>
    )
}