import React, { Component } from "react";
import "./ComponentCard.css";


export default function BitbakeComponentCard({ id, name, license_number, osv_vuln_number, bdu_vuln_number, picked = false, onClick }) {
    if (!picked) {
        picked = "bitbakeComponentCard"
    } else {
        picked = "bitbakeComponentCardPicked"
    }
    return (
        <>
            <div id={id} className={picked} onClick={onClick}>
                <div className="bitbakeComponentName">
                    <p className="bitbakeComponentName">{name}</p>
                </div>
                <div className="bitbakeComponentStatus">
                </div>
                <div className="bitbakeComponentStatus">
                    <p className="bitbakeComponentLicenseFaded">Лицензии: </p>{license_number}
                    <p className="bitbakeComponentLicenseFaded"> CVE: </p>{osv_vuln_number}
                    <p className="bitbakeComponentLicenseFaded">БДУ ФСТЭК: </p>{bdu_vuln_number}
                </div>
            </div>
        </>
    )
}