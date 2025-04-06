import React, { useState, useRef } from "react";
import { Viewer } from "@microsoft/sarif-web-component";
import "./Sarif.css";
import Button from "../Button/Button";

export default function SarifViewer() {
    const [report, setReport] = useState(null);
    const fileInputRef = useRef(null);

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                try {
                    const parsedReport = JSON.parse(e.target.result);
                    setReport(parsedReport);
                } catch (error) {
                    console.error("Ошибка при разборе SARIF-файла:", error);
                    alert("Неверный формат SARIF-файла.");
                }
            };
            reader.readAsText(file);
        }
    };

    const handleReset = () => {
        setReport(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    return (
        <>
            <div className="sarifMenu">
                <div className="sarifUpload">
                    <h4>Посмотреть локальный отчёт</h4>
                    <input
                        ref={fileInputRef}
                        className="sarif"
                        type="file"
                        accept=".sarif,.json"
                        onChange={handleFileUpload}
                    />
                </div>
                <div className="sarifSelect">
                    <h4>Посмотреть отчёт с сервера</h4>
                </div>
                <div className="sarifReset">
                    <Button
                        style={"projectClose"}
                        type={"submit"}
                        onClick={handleReset}
                    >
                        Сбросить
                    </Button>
                </div>
            </div>
            <div className="sarifViewer">
                {report && <Viewer logs={[report]} />}
            </div>
        </>
    );
}