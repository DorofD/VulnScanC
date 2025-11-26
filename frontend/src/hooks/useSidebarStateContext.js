import React, { useContext } from "react";
import { SidebarStateContext } from "../contexts/SidebarStateContext";

export const useSidebarState = () => useContext(SidebarStateContext) 