import React, { useEffect, useState } from "react";
import "./ColorSchemeSelector.css"
import { useColorScheme } from "../../hooks/useColorThemeContext";
import MoonIcon from "../../svg_images/Moon.svg"
import SunIcon from "../../svg_images/Sun.svg"

export default function ColorSchemeSelector() {
    const { colorScheme, setColorScheme } = useColorScheme();

    return (
        <div className="colorSchemeIcons">
            {colorScheme == 'default' &&
                <MoonIcon className="colorSchemeIconStyle" onClick={() => {
                    setColorScheme('dark-red');
                    localStorage.setItem("colorScheme", 'dark-red')
                }} />
            }
            {colorScheme == 'dark-red' &&
                <SunIcon className="colorSchemeIconStyle" onClick={() => {
                    setColorScheme('default');
                    localStorage.setItem("colorScheme", 'default')
                }} />
            }
        </div>

    );
}

