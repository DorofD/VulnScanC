import React from "react";
import { useState, useEffect, useContext} from "react";
import { apiGetBinaryInfo, apiBuildBinary, apiGetBinaryFile } from "../../services/apiBinary";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import "./Binary.css"
import Loader from "../Loader/Loader";

export default function Binary() {

    const { notificationData, setNotificationData, toggleNotificationFunc, notificationToggle } = useNotificationContext();
    const [ loaderActive, setLoaderActive ] = useState(false)

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
            {buildInProcess &&  <Loader />}
            <div className="binaryContainer">
            <div className="binaryHeader">
                <button onClick={() => buildBinary()}> Собрать исполняемый модуль </button>
                <button onClick={() => getBinaryFile()}> Загрузить исполняемый модуль </button>
            </div>
            {loading === 'loading' && <Loader />}
            {loading === 'error' && <p> бекенд отвалился</p>}
            {loading === 'loaded' && <>
                <div className="binaryBottom">

                      <p className="binaryFaded">Файл: </p> {binaryInfo.binary_file && binaryInfo.binary_file || "Модуль не найден"}
                      <p className="binaryFaded">Время сборки: </p> {binaryInfo.change_time && binaryInfo.change_time || "Модуль не найден"}
                        <p>Лог сборки: </p>
            
                        <div className="binaryContent">{binaryInfo.build_log_data && binaryInfo.build_log_data  || "Сборочный лог не найден"}</div>
                </div>
                    </>}
        </div>
    </>
    
    );
}