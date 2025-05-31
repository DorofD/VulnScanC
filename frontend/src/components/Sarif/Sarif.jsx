import React, { useState, useRef, useEffect } from "react";
import { Viewer } from "@microsoft/sarif-web-component";
import { apiGetSarifFile, apiGetSarifFilesList, apiDeleteSarifFile } from "../../services/apiSarif";
import "./Sarif.css";
import SarifFileCard from "./SarifFileCard/SarifFileCard";
import Button from "../Button/Button";
import Loader from "../Loader/Loader";

export default function SarifViewer() {
    const [loaderActive, setLoaderActive] = useState(false)
    const [loading, setLoading] = useState('loading')

    const [files, setFiles] = useState([])
    const [pickedFile, setPickedFile] = useState('')
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
        setPickedFile('')
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };


    async function getSarifFilesList() {
        try {
            setLoading('loading')
            const files = await apiGetSarifFilesList()
            if (Array.isArray(files)) {
                setFiles(files);
            } else {
                console.error('Received data is not an array', files);
                setFiles([]);
            }
            setLoading('loaded')
        } catch (err) {
            setLoading('error')
        }
    }

    async function showSarifFile(filename) {
        try {
            setLoaderActive(true)
            console.log(filename);
            const file = await apiGetSarifFile(filename);

            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    try {
                        const parsedReport = JSON.parse(event.target.result);
                        setReport(parsedReport);
                    } catch (error) {
                        console.error("Ошибка при разборе SARIF-файла:", error);
                        alert("Неверный формат SARIF-файла.");
                        setLoaderActive(false)
                    }
                };
                reader.readAsText(file);
                setLoaderActive(false)
            }

            setLoading('loaded');
        } catch (err) {
            setLoading('error');
            console.error(err);
        }
    }

    useEffect(() => {
        getSarifFilesList()
    }, [])

    return (
        <>
            {loaderActive && <Loader></Loader> || <></>}
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
                    {loading === 'loading' && <Loader />}
                    {loading === 'error' && <>бекенд отвалился</>}
                    {loading === 'loaded' && <>
                        {files.map(file =>
                            <SarifFileCard id={file}
                                name={file}
                                picked={pickedFile === file && true || false}
                                onClick={() => { handleReset(); setPickedFile(file); showSarifFile(String(file)) }}>
                            </SarifFileCard>)}
                    </>}
                    {loading === 'loaded' && !files && <>Файлы не были найдены, либо переданы в приложение некорректно</>}
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