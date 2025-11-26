import React, { useContext } from "react";
import { NotificationContext } from "../contexts/NotificationContext";

export const useNotificationContext = () => useContext(NotificationContext)