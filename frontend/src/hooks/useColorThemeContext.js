import React, { useContext } from "react";
import { ColorSchemeContext } from "../contexts/ColorSchemeContext";

export const useColorScheme = () => useContext(ColorSchemeContext) 