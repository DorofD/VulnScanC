import React, { useContext } from "react";
import { TimedMessagesContext } from "../contexts/TimedMessagesContext";

export const useTimedMessagesContext = () => useContext(TimedMessagesContext)