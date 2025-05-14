import React, { Component } from "react";
import "./CommentCard.css";
import Button from "../../Button/Button";

export default function CommentCard({id, onClick, picked = false, user, datetime, text, deleteFunction, owner }) {
    let cardStyle
    let contentStyle
    if (!picked) {
        cardStyle = "commentCard"
        contentStyle = "commentContent"
    } else {
        cardStyle = "commentCardPicked"
        contentStyle = "commentContentPicked"
    }

    return (
        <div id={id} className={cardStyle} onClick={!picked && onClick || (() =>{})}>
            {picked && 
                <div className="commentCardClose">
                    {owner && <Button style={"commentsCardClose"} onClick={deleteFunction}>Удалить</Button>}
                    <Button style={"commentsCardClose"} onClick={onClick}>Закрыть</Button>
                </div>}
            {owner && <><p className="commentFaded"> </p><b>Вы </b><p className="commentFaded">добавили комментарий</p> {datetime}</> 
            || <><p className="commentFaded"> </p><b>{user}</b> <p className="commentFaded">добавил комментарий</p> {datetime}</> }
            <br />
            <br />

            <div className={contentStyle}>{text}</div>
        </div>
    )
}