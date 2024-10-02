import React from "react";
import { useState, useEffect, useContext} from "react";
import { apiGetBinaryInfo, apiBuildBinary, apiGetBinaryFile } from "../../services/apiBinary";
import Button from "../Button/Button";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import BinaryCard from "./BinaryCard/BinaryCard";
import "./Binary.css"

export default function Binary() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();

    const [loading, setLoading] = useState('loading')
    const [binaryInfo, setBinaryInfo] = useState([])
    const [isPicked, setIsPicked] = useState(false)
    const [buildInProcess, setBuildInProcess] = useState(false)

    async function getBinaryInfo() {
        try {
            setLoading('loading')
            const response = await apiGetBinaryInfo()
            const info = await response.json()
            setBinaryInfo(info);
            setLoading('loaded')
        } catch (err) {
            console.log(err)
            setLoading('error')
        }
    }

    async function buildBinary() {
        try {
            setBuildInProcess(true)
            const response = await apiBuildBinary()
            if (response.status == 200) {
                setIsPicked(false)
                getBinaryInfo()
                setBuildInProcess(false)
                setNotificationData({message:'Исполняемый модуль собран', type: 'success'})
                toggleNotificationFunc()
            } else {
                setBuildInProcess(false)
                setNotificationData({message:'Исполняемый модуль не собран', type: 'error'})
                toggleNotificationFunc()
            }
        } catch (err) {
            setNotificationData({message: `Проблема с бекендом: ${err}`, type: 'error'})
            toggleNotificationFunc()
        }
    }

    async function getBinaryFile() {
        try {
            const report = await apiGetBinaryFile()
        } catch (err) {
            setNotificationData({message:'Не удалось загрузить исполняемый модуль', type: 'error'})
            toggleNotificationFunc()
        }
    }
    
    useEffect(() => {
        getBinaryInfo()
    }, [])

    return (
    <>
        <div className="logs">

            <div className="logsHeader">
                <Button style={"buildBinary"} onClick={() => buildBinary()}> Собрать исполняемый модуль </Button>
                <Button style={"buildBinary"} onClick={() => getBinaryFile()}> Загрузить исполняемый модуль </Button>
            {buildInProcess && <p>Выполняется сборка исполняемого модуля...</p>}
            </div>
            {loading === 'loading' && <p> Loading ...</p>}
            {loading === 'error' && <p> бекенд отвалился</p>}
            {loading === 'loaded' && <>

                        <BinaryCard
                        id={0}
                        file={binaryInfo.binary_file && binaryInfo.binary_file || "Модуль не найден"}
                        datetime={binaryInfo.change_time && binaryInfo.change_time || "Модуль не найден"}
                        note={binaryInfo.build_log_data && binaryInfo.build_log_data  || "Сборочный лог не найден"}
                        picked={isPicked}
                        onClick={() => {
                          if (!isPicked) {
                            setIsPicked(true);
                          } else {
                            setIsPicked(false);
                          }
                        }}
                      />
                    </>}
        </div>
    </>
    );
}