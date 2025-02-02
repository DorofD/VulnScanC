import React, { Component} from "react";
import Button from "../../Button/Button";
import "./BinaryCard.css";


export default function BinaryCard({ id, datetime, file, note, picked, onClick }) {
    let cardStyle
    let contentStyle

    if (!picked) {
        cardStyle = "binaryCard"
        contentStyle = "logContent"
    } else {
        cardStyle = "binaryCardPicked"
        contentStyle = "binaryContentPicked"
    }

    return (

        <div id={id} className={cardStyle} onClick={!picked && onClick || (() =>{})}>
            {picked && 
                <div className="binaryCardClose">
                    <Button style={"logsCardClose"} onClick={onClick}>X</Button>
                </div>}
            <p className="binaryFaded">Файл: </p> {file} <p className="binaryFaded">Время сборки: </p> {datetime}
            <p>Лог сборки: </p>
            
            <div className={contentStyle}>{note}</div>
        </div>
    );
}