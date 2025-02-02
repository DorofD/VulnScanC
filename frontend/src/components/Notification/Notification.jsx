import React, { Component } from "react";
import "./Notification.css";
import { useNotificationContext } from "../../hooks/useNotificationContext";



export default function Notification () {
    
    const {notificationData, notificationToggle} = useNotificationContext();

    const message = notificationData['message']
    const type = notificationData['type']
    
    if (!message) return (<></>);

    return (
      <div className={'notification ' + type} key={notificationToggle} >
        {message}
      </div>
    );
};